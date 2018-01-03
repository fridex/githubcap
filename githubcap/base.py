"""Base classes for resource and resource handler classes."""

import copy
from datetime import datetime
import enum
import logging
import time
import typing

import requests

import attr
from voluptuous import Schema
from voluptuous import ScalarInvalid
from voluptuous import MultipleInvalid

from .configuration import Configuration
from .configuration import ConfigurationDefaults
from .enums import GitHubCapEnum
from .exceptions import HTTPError
from .exceptions import MissingPassword
from .exceptions import SchemaValidationError
from .utils import dict2json
from .utils import next_pagination_page
from .utils import parse_datetime
from .utils import serialize_datetime

_LOG = logging.getLogger(__name__)


@attr.s
class GitHubHandlerBase(object):
    """A base class for handler implementation."""

    DEFAULT_PER_PAGE: typing.ClassVar[int] = ConfigurationDefaults.PER_PAGE_LISTING

    @classmethod
    def _call(cls, uri: str, payload: dict = None, method: str = None):
        """Perform a request to GitHub API v3.

        :param uri: API endpoint
        :param payload: data sent to GitHub API remote
        :param method: a string representation of method that should be used
        """
        requests_kwargs = {
            'headers': copy.copy(Configuration().headers)
        }

        if Configuration().token:
            _LOG.debug("Using OAuth2 token '%s***' for GitHub call", Configuration().token[:4])
            requests_kwargs['headers']['Authorization'] = 'token {!s}'.format(Configuration().token)
        elif Configuration().user:
            if not Configuration().password:
                raise MissingPassword("No password set for user {!s}".format(Configuration().user))

            _LOG.debug("Using basic authentication for user %s", Configuration().user)
            requests_kwargs['auth'].append((Configuration().user, Configuration().password))
        else:
            _LOG.debug("No authentication is used")

        url = "{!s}/{!s}".format(Configuration().github_api, uri)
        requests_func = getattr(requests, method.lower())
        if payload:
            requests_kwargs['json'] = payload

        while True:
            _LOG.debug("%s %s", method, url)
            response = requests_func(url, **requests_kwargs)

            _LOG.debug("Request took %s and the HTTP status code for response was %d",
                       response.elapsed, response.status_code)

            if not (response.status_code == 403 and
                    response.json()['message'].startswith("API rate limit exceeded") and
                    Configuration().omit_rate_limiting):
                break

            reset_datetime = datetime.fromtimestamp(int(response.headers['X-RateLimit-Reset']))
            sleep_time = (reset_datetime - datetime.now()).total_seconds()
            _LOG.debug("API rate limit hit, retrying in %d seconds...", sleep_time)
            time.sleep(sleep_time)

        try:
            # Rely on request's checks here
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise HTTPError(response.json(), response.status_code) from exc

        return response.json(), response.headers

    def _get_query_string(self):
        """Construct query string added to URL."""
        raise NotImplementedError

    def _do_listing(self, base_uri: str):
        """Perform listing of entries returned from API endpoint - respect pagination if configured."""
        while True:
            uri = '{!s}?{!s}'.format(base_uri, self._get_query_string())
            response, headers = self._call(uri, method='GET')

            for entry in response:
                yield entry

            if not Configuration().pagination:
                return

            next_page = next_pagination_page(headers)
            if next_page is None:
                return
            # TODO: create a new class that has "page"
            self.page = next_page

    @classmethod
    def submit(cls, item):
        """Submit an item to remote."""
        raise NotImplementedError


@attr.s
class GitHubBase(object):
    """Base class for resources provided by GitHub API v3."""

    _SCHEMA: typing.ClassVar[Schema] = None

    # TODO: dirty flag

    @staticmethod
    def _report_schema_errors(response: dict, exc: Exception) -> None:
        """Report schema errors in a human readable fashion."""
        if not isinstance(exc, MultipleInvalid):
            return

        for error in exc.errors:
            if not isinstance(error, ScalarInvalid):
                continue

            value = response
            for key in error.path:
                value = value[key]
            _LOG.error("Unknown value in %s: %r", error.path, value)

    @classmethod
    def from_response(cls, response: dict):
        """Parse resource from GitHub API response."""
        if cls._SCHEMA is None:
            raise NotImplementedError("No schema defined for entity {!r}".format(cls.__name__))

        if Configuration().validate_schemas:
            try:
                cls._SCHEMA(response)  # pylint: disable=not-callable
            except Exception as exc:
                _LOG.debug(dict2json(response))
                cls._report_schema_errors(response, exc)
                raise SchemaValidationError("Failed to validate schema for {!r}".format(cls.__name__)) from exc

        return cls.from_dict(response)

    @classmethod
    def _from_dict_value(cls, attribute_type: attr.Attribute, value: typing.Any) -> typing.Any:
        """Translate value to it's actual representation based on resource type defined."""
        # pylint: disable=protected-access
        if attribute_type == datetime:
            return parse_datetime(value)
        elif issubclass(attribute_type, GitHubCapEnum):
            return attribute_type.from_value(value)
        elif issubclass(attribute_type, GitHubBase):
            return attribute_type.from_dict(value)
        elif '_gorg' in attribute_type.__dict__ and attribute_type._gorg == typing.List:
            assert len(attribute_type.__args__) == 1,\
                "Type defined multiple types: {!r}".format(attribute_type)  # Ignore B101
            return list(cls._from_dict_value(attribute_type.__args__[0], item) for item in value)

        return value

    @classmethod
    def from_dict(cls, dict_: dict):
        """Create resource instance from a dictionary."""
        if dict_ is None:
            return None

        values = {}
        for attribute in cls.__attrs_attrs__:  # pylint: disable=no-member
            if attribute.name in dict_:
                values[attribute.name] = cls._from_dict_value(attribute.type, dict_[attribute.name])

        return cls(**values)

    @classmethod
    def _to_dict_value(cls, value: typing.Any) -> typing.Union[str, typing.List[str]]:
        """Serialize resource value to based on it's type."""
        if isinstance(value, datetime):
            return serialize_datetime(value)
        elif isinstance(value, GitHubBase):
            return value.to_dict()
        elif issubclass(value.__class__, enum.Enum):
            return value.value
        elif isinstance(value, list):
            return list(cls._to_dict_value(item) for item in value)

        return value

    def to_dict(self) -> dict:
        """Create a dictionary representation of a resource."""
        result = {}
        for attribute in self.__attrs_attrs__:  # pylint: disable=no-member
            result[attribute.name] = self._to_dict_value(getattr(self, attribute.name))
        return result

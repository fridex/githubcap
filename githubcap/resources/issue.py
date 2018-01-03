"""GitHub issue creation and manipulation."""

from datetime import datetime
import typing

import attr
from voluptuous import Schema

from githubcap.base import GitHubBase
from githubcap.base import GitHubHandlerBase
from githubcap.enums import AuthorAssociation
from githubcap.enums import Filtering
from githubcap.enums import Sorting
from githubcap.enums import SortingDirection
from githubcap.enums import State
from githubcap.schemas import ISSUE_SCHEMA
from githubcap.utils import serialize_datetime

from .label import Label
from .milestone import Milestone
from .repository import Repository
from .user import User


@attr.s
class IssuePullRequestInfo(GitHubBase):
    """Representation of pull request details in case of issue is a pull request."""

    url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    diff_url = attr.ib(type=str)
    patch_url = attr.ib(type=str)


@attr.s
class Issue(GitHubBase):
    """Representation of an issue."""

    _SCHEMA: typing.ClassVar[Schema] = ISSUE_SCHEMA

    id = attr.ib(type=int)
    url = attr.ib(type=str)
    labels_url = attr.ib(type=str)
    comments_url = attr.ib(type=str)
    events_url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    number = attr.ib(type=int)
    state = attr.ib(type=State)
    title = attr.ib(type=str)
    body = attr.ib(type=str)
    user = attr.ib(type=User)
    locked = attr.ib(type=bool)
    comments = attr.ib(type=int)
    labels = attr.ib(type=typing.List[Label])
    author_association = attr.ib(type=AuthorAssociation)
    assignees = attr.ib(type=typing.List[User])
    milestone = attr.ib(type=Milestone)
    closed_at = attr.ib(type=datetime)
    created_at = attr.ib(type=datetime)
    updated_at = attr.ib(type=datetime)

    repository = attr.ib(type=Repository, default=None)
    closed_by = attr.ib(type=User, default=None)
    pull_request = attr.ib(type=IssuePullRequestInfo, default=None)

    @classmethod
    def from_dict(cls, dict_: dict):
        """Construct :class:githubcap.resources.issue.Issue from a dictionary."""
        dict_.pop('assignee', None)  # Deprecated entry, remove it.
        return super().from_dict(dict_)

    def is_pull_request(self) -> bool:
        """Check whether this issue is a pull request."""
        return self.pull_request is not None


@attr.s
class IssueHandler(GitHubHandlerBase):
    """Handle issue creation and modification."""

    title = attr.ib(type=str)
    body = attr.ib(type=str)
    milestone = attr.ib(type=int, default=None)
    labels = attr.ib(type=typing.List[Label], default=attr.Factory(list))
    assignees = attr.ib(type=typing.List[User], default=attr.Factory(list))
    state = attr.ib(default=State.get_default(), type=State)

    @classmethod
    def by_number(cls, organization: str, project: str, number: int) -> Issue:
        """Retrieve issue based on it's number."""
        uri = 'repos/{org!s}/{project!s}/issues/{number:d}'.format(org=organization, project=project, number=number)
        response, _ = cls._call(uri, method='GET')
        return Issue.from_response(response)

    def create(self, organization: str, project: str) -> Issue:
        """Create an issue."""
        uri = 'repos/{org!s}/{project!s}/issues'.format(org=organization, project=project)
        payload = {key: value for key, value in attr.asdict(self).items() if value is not None}
        response, _ = self._call(uri, payload=payload, method='POST')
        return Issue.from_response(response)

    def edit(self, organization: str, project: str, number: int) -> Issue:
        """Edit existing issue."""
        uri = 'repos/{org!s}/{project!s}/issues/{number:d}'.format(org=organization, project=project, number=number)
        payload = {key: value for key, value in attr.asdict(self).items() if value is not None}
        response, _ = self._call(uri, payload=payload, method='PATCH')
        # TODO: report not-changed values
        return Issue.from_response(response)


@attr.s
class IssuesHandler(GitHubHandlerBase):
    """Handling issues querying."""

    page = attr.ib(default=1, type=int)
    per_page = attr.ib(default=GitHubHandlerBase.DEFAULT_PER_PAGE, type=int)
    filter = attr.ib(default=Filtering.get_default(), type=Filtering)
    state = attr.ib(default=State.get_default(), type=State)
    labels = attr.ib(default=attr.Factory(list), type=typing.List[Label])
    sort = attr.ib(default=Sorting.get_default(), type=Sorting)
    direction = attr.ib(default=SortingDirection.get_default(), type=SortingDirection)
    since = attr.ib(default=None, type=str)
    milestone = attr.ib(default=attr.Factory(lambda: '*'), type=str)

    assignee = attr.ib(default=attr.Factory(lambda: '*'), type=str)
    creator = attr.ib(default=None, type=str)
    mentioned = attr.ib(default=None, type=str)

    @milestone.validator
    def milestone_validator(self, _, value: typing.Any) -> None:  # pylint: disable=no-self-use
        """Validate supplied milestone number value."""
        if isinstance(value, int):
            if value < 0:
                raise ValueError("Integer representation of a milestone has to be non-negative integer")
        elif not isinstance(value, str) and value is not None:
            raise ValueError("Unknown milestone representation supplied {!r} of type {!s}".format(value, type(value)))

    def _get_query_string(self) -> str:
        """Get query string for parametrized queries."""
        ret = ''
        for key, value in attr.asdict(self).items():
            if key == 'since':
                if value is None:
                    continue

                if isinstance(value, datetime):
                    value = serialize_datetime(value)

            if key in ('assignee', 'creator', 'mentioned') and value is None:
                continue

            if key == 'labels':
                if not value:
                    continue
                value = ",".join(value)

            if ret:
                ret += '&'

            ret += '{!s}={!s}'.format(key, str(value) if value is not None else 'none')
        return ret

    def list_assigned_issues(self, organization: str = None) -> Issue:
        """List all assigned issues for the given organization - if organization is None, all issues are listed."""
        if organization:
            base_uri = 'orgs/{!s}/issues'.format(organization)
        else:
            base_uri = 'issues'

        for item in self._do_listing(base_uri):
            yield Issue.from_response(item)

    def list_issues(self, organization: str, project: str) -> Issue:
        """List issues for the given organization/owner and project."""
        if project is None:
            # TODO: raise something meaningful
            raise ValueError
        base_uri = 'repos/{!s}/{!s}/issues'.format(organization, project)
        for item in self._do_listing(base_uri):
            yield Issue.from_response(item)

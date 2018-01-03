"""A library level configuration for githubcap."""

import contextlib
import logging
import os
import typing

import yaml

import attr

from .exceptions import ConfigNotFound
from .exceptions import ConfigurationError

_LOG = logging.getLogger(__name__)

_CONFIGURATION_FILE_HEADER = """# Configuration file for githubcap in YAML language.
#
# It is *NOT* recommended to store password in a plain text - please use
# a token that is preferred authentication method, which also works with
# two factor authentication.
#
# Refer to githubcap documentation for more configuration info:
#   https://githubcap.readthedocs.org/en/latest/configuration.html
#
---
"""


class ConfigurationDefaults:  # pylint: disable=too-few-public-methods
    """Default values for configuration."""

    CONFIG_FILE_PATH = os.path.join(os.getenv('HOME'), '.config', 'githubcap', 'config.yaml')
    HEADERS = {}
    USER = None
    PASSWORD = None
    TOKEN = None
    PER_PAGE_LISTING = 100
    GITHUB_API = os.getenv('GITHUB_API', 'https://api.github.com')
    OMIT_RATE_LIMITING = False
    PAGINATION = True
    VALIDATE_SCHEMAS = True
    GITHUB_DOCS = os.getenv('GITHUB_DOCS', 'https://developer.github.com')
    GITHUB_DOCS_V3 = os.getenv('GITHUB_DOCS_VERSION', 'v3')


@attr.s(slots=True)
class _ConfigurationSingleton(object):
    """A library level singleton for storing configuration options."""

    # It's ok not to have factories here, this is a singleton.
    headers = attr.ib(default=ConfigurationDefaults.HEADERS, type=dict)
    user = attr.ib(default=ConfigurationDefaults.USER, type=str)
    password = attr.ib(default=ConfigurationDefaults.PASSWORD, type=str)
    token = attr.ib(default=ConfigurationDefaults.TOKEN, type=str)
    per_page_listing = attr.ib(default=ConfigurationDefaults.PER_PAGE_LISTING, type=int)
    github_api = attr.ib(default=ConfigurationDefaults.GITHUB_API, type=str)
    omit_rate_limiting = attr.ib(default=ConfigurationDefaults.OMIT_RATE_LIMITING, type=bool)
    pagination = attr.ib(default=ConfigurationDefaults.PAGINATION, type=bool)
    validate_schemas = attr.ib(default=ConfigurationDefaults.VALIDATE_SCHEMAS, type=bool)
    github_docs = attr.ib(default=ConfigurationDefaults.GITHUB_DOCS, type=str)
    github_docs_version = attr.ib(default=ConfigurationDefaults.GITHUB_DOCS_V3, type=str)

    @per_page_listing.validator
    def per_page_listing_validator(self, _, value):  # pylint: disable=no-self-use
        """Validate supplied per page configuration option."""
        if not 1 <= value <= 100:
            raise ConfigurationError("Page listing has to be between 1 and 100.")

    @contextlib.contextmanager
    def temporary_change(self, **adjusted_options):  # pylint: disable=no-self-use
        """Temporary change configuration options - old configuration options are yield.

        >>> from githubcap import Configuration
        >>> from githubcap.resources import IssueHandler
        >>> with Configuration().temporary_change(pagination=10, validate_schemas=False):
        >>>     IssueHandler.by_number(organization='selinon', project='selinon', number=1)
        """
        option_backup = {}
        config = Configuration()

        for option, value in adjusted_options.items():
            option_backup[option] = getattr(config, option)
            setattr(Configuration(), option, value)

        yield option_backup

        for option, value in option_backup.items():
            setattr(config, option, value)

    @classmethod
    def from_config_file(cls, config_file_path: typing.Optional[str] = None) -> None:
        """Initialize configuration from a configuration file (YAML format)."""
        config_file_path = config_file_path or ConfigurationDefaults.CONFIG_FILE_PATH
        try:
            with open(config_file_path) as config_file:
                configuration = yaml.safe_load(config_file)
        except FileNotFoundError as exc:
            raise ConfigNotFound("No configuration present in {!s}".format(config_file_path)) from exc
        except Exception as exc:
            raise ConfigurationError("Unable to open configuration: {!s}".format(str(exc))) from exc

        try:
            instance = cls(**configuration)
            _LOG.debug("Configuration successfully loaded from file %r", config_file_path)
            return instance
        except TypeError as exc:
            raise ConfigurationError("Unknown configuration option: {!s}".format(str(exc))) from exc
        except Exception as exc:
            raise ConfigurationError("Failed to initialize configuration: {!s}".format(str(exc))) from exc

    def to_dict(self) -> dict:
        """Represent configuration in a dict."""
        return attr.asdict(self)

    def write2file(self, file_path: typing.Optional[str] = None, overwrite: typing.Optional[bool] = False) -> None:
        """Write configuration to a YAML file."""
        file_path = file_path or ConfigurationDefaults.CONFIG_FILE_PATH

        if not file_path.endswith(('.yaml', '.yml')):
            file_path += '.yaml'

        if os.path.isfile(file_path) and not overwrite:
            raise ConfigurationError("Configuration file already present (overwrite flag was not set)")

        # Create directory structure first.
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(file_path, 'w') as config_file:
            config_file.write(_CONFIGURATION_FILE_HEADER)
            yaml.dump(self.to_dict(), config_file)
            _LOG.info("Configuration file written to %r", file_path)

    @classmethod
    def get_configuration(cls, config_file_path: typing.Optional[str] = None):
        """Get configuration instance (used only in :class:githubcap.configuration.Configuration)."""
        try:
            return cls.from_config_file(config_file_path)
        except ConfigNotFound as exc:
            if config_file_path is not None:
                raise
            _LOG.debug("Fallback to default configuration: %s", exc)

        return cls()


class Configuration(object):  # pylint: disable=too-few-public-methods
    """A library level configuration."""

    _instance = None

    def __init__(self, config_file=None, **kwargs):
        """Initialize configuration if not done so already."""
        if Configuration._instance is None:
            Configuration._instance = _ConfigurationSingleton.get_configuration(config_file)
        elif config_file is not None:
            # Prevent from potentially weird behaviour.
            raise ConfigurationError("Configuration already instantiated, initialize configuration from a "
                                     "custom file before first configuration access.")

        for key, value in kwargs.items():
            setattr(Configuration._instance, key, value)

    def __str__(self):
        """Represent Configuration as a string - wraps singleton."""
        return str(Configuration._instance)

    def __repr__(self):
        """Represent Configuration - wraps singleton."""
        return repr(Configuration._instance)

    def __getattr__(self, item):
        """Override access so items are retrieved from singleton."""
        if item == 'instance':
            return self._instance

        try:
            return getattr(Configuration._instance, item)
        except AttributeError as exc:
            raise ConfigurationError("Unknown configuration option '{!s}'".format(item)) from exc

    def __setattr__(self, key, value):
        """Override assigning items so items assigned in singleton."""
        if key == '_instance':
            return super().__setattr__(key, value)
        try:
            return setattr(Configuration._instance, key, value)
        except AttributeError as exc:
            raise ConfigurationError("Unknown configuration option '{!s}'".format(key)) from exc

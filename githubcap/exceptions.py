"""Exceptions that are raised inside library."""


class GithubcapException(Exception):
    """Base class for githubcap exception tree."""


class ConfigNotFound(GithubcapException):
    """Raised on non-existing configuration file."""


class ConfigurationError(GithubcapException):
    """Raised on invalid configuration."""


class MissingPassword(GithubcapException):
    """Raised when a user name is set but no password provided."""


class HTTPError(GithubcapException):
    """Raised on unrecoverable HTTP errors."""

    def __init__(self, message: dict, status_code: int):
        """Initialize HTTP error exception."""
        super().__init__(message['message'])

        self.status_code = status_code
        self.raw_response = message


class SchemaValidationError(GithubcapException):
    """Raised on schema validation failure."""

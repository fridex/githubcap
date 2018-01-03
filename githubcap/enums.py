"""Representation of enums that are present at GitHub API v3."""

from enum import Enum
from typing import List


class GitHubCapEnum(Enum):
    """A base class for defined enums."""

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        raise NotImplementedError

    @classmethod
    def all_names(cls) -> List[str]:
        """Get a list of all enum names."""
        return list(member_name for member_name in cls.__members__.keys())

    @classmethod
    def all_values(cls) -> List[str]:
        """Get a list of all enum values."""
        return list(member.value for member in cls.__members__.values())

    def __str__(self) -> str:
        """Get a string representation of an enum."""
        return self.value

    @classmethod
    def from_str(cls, name: str):
        """Get enum based on its string representation."""
        return cls.__members__[name]

    @classmethod
    def from_value(cls, value: str):
        """Get enum based on its value."""
        return cls._value2member_map_[value]


class Filtering(GitHubCapEnum):
    """Issue filtering."""

    ASSIGNED = 'assigned'
    CREATED = 'created'
    MENTIONED = 'mentioned'
    SUBSCRIBED = 'subscribed'
    ALL = 'all'

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        return cls.ALL


class State(GitHubCapEnum):
    """Resource state representation (e.g. for issues)."""

    OPEN = 'open'
    CLOSED = 'closed'
    ALL = 'all'

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        return cls.ALL


class Sorting(GitHubCapEnum):
    """Sorting criteria for issues."""

    CREATED = 'created'
    UPDATED = 'updated'
    COMMENTS = 'comments'

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        return cls.CREATED


class SortingDirection(GitHubCapEnum):
    """Sorting direction criteria."""

    ASC = 'asc'
    DESC = 'desc'

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        return cls.DESC


class AuthorAssociation(GitHubCapEnum):
    """Author association for a resource (e.g. an issue)."""

    OWNER = 'OWNER'
    CONTRIBUTOR = 'CONTRIBUTOR'
    MEMBER = 'MEMBER'
    COLLABORATOR = 'COLLABORATOR'
    FIRST_TIME_CONTRIBUTOR = 'FIRST_TIME_CONTRIBUTOR'
    NONE = 'NONE'

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        return cls.NONE


class UserType(GitHubCapEnum):
    """Type of a GitHub user."""

    USER = 'User'
    ORGANIZATION = 'Organization'

    @classmethod
    def get_default(cls):
        """Get default enum value."""
        return cls.USER

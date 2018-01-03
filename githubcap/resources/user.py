"""User representation and account modifications."""

import typing

import attr
from voluptuous import Schema

from githubcap.base import GitHubBase
from githubcap.base import GitHubHandlerBase
from githubcap.enums import UserType
from githubcap.schemas import USER_SCHEMA


@attr.s
class User(GitHubBase):
    """Representation of a GitHub user."""

    _SCHEMA: typing.ClassVar[Schema] = USER_SCHEMA

    login = attr.ib(type=str)
    id = attr.ib(type=int)
    avatar_url = attr.ib(type=str)
    gravatar_id = attr.ib(type=str)
    url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    followers_url = attr.ib(type=str)
    following_url = attr.ib(type=str)
    gists_url = attr.ib(type=str)
    starred_url = attr.ib(type=str)
    subscriptions_url = attr.ib(type=str)
    organizations_url = attr.ib(type=str)
    repos_url = attr.ib(type=str)
    events_url = attr.ib(type=str)
    received_events_url = attr.ib(type=str)
    type = attr.ib(type=UserType)
    site_admin = attr.ib(type=bool)


@attr.s
class UserHandler(GitHubHandlerBase):
    """Handle actions on user account."""

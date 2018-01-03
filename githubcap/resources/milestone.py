"""A milestone representation and interaction."""

from datetime import datetime
import typing

import attr
from voluptuous import Schema

from githubcap.base import GitHubBase
from githubcap.base import GitHubHandlerBase
from githubcap.enums import State
from githubcap.schemas import MILESTONE_SCHEMA

from .user import User


@attr.s
class Milestone(GitHubBase):
    """A milestone representation."""

    _SCHEMA: typing.ClassVar[Schema] = MILESTONE_SCHEMA

    url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    labels_url = attr.ib(type=str)
    id = attr.ib(type=int)
    number = attr.ib(type=int)
    state = attr.ib(type=State)
    title = attr.ib(type=str)
    description = attr.ib(type=str)
    creator = attr.ib(type=User)
    open_issues = attr.ib(type=int)
    closed_issues = attr.ib(type=int)
    created_at = attr.ib(type=datetime)
    updated_at = attr.ib(type=datetime)
    closed_at = attr.ib(type=datetime)
    due_on = attr.ib(type=datetime)


@attr.s
class MilestoneHandler(GitHubHandlerBase):
    """Handle creation and modification of milestones."""

    # TODO: implement

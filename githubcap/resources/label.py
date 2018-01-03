"""A label representation, creation and modification."""

import typing

import attr
from voluptuous import Schema

from githubcap.base import GitHubBase
from githubcap.base import GitHubHandlerBase
from githubcap.schemas import LABEL_SCHEMA


@attr.s
class Label(GitHubBase):
    """Representation of an issue label."""

    _SCHEMA: typing.ClassVar[Schema] = LABEL_SCHEMA

    id = attr.ib(type=int)
    url = attr.ib(type=str)
    name = attr.ib(type=str)
    color = attr.ib(type=str)
    default = attr.ib(type=bool)


@attr.s
class LabelHandler(GitHubHandlerBase):
    """Manipulation of issue labels."""

    # TODO: implement

"""License representation and manipulation."""

import attr

from githubcap.base import GitHubBase
from githubcap.base import GitHubHandlerBase


class License(GitHubBase):
    """GitHub license representation."""

    key = attr.ib(type=str)
    name = attr.ib(type=str)
    spdx_id = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class LicenseHandler(GitHubHandlerBase):
    """Manipulation of repository license."""

    # TODO: implement

"""A GitHub user schema."""

from voluptuous import Any
from voluptuous import Required
from voluptuous import Url

# pylint: disable=no-value-for-parameter


LICENSE_SCHEMA = {
    Required("key"): str,
    Required("name"): str,
    Required("spdx_id"): Any(str, None),
    Required("url"): Any(Url(), None)
}

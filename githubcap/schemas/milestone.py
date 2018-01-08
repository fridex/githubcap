"""Issue milestone schema."""

from voluptuous import Any
from voluptuous import Required
from voluptuous import Schema
from voluptuous import Url

from githubcap.enums import State

from .user import USER_SCHEMA

# pylint: disable=no-value-for-parameter


MILESTONE_SCHEMA = Schema({
    Required("url"): Url(),
    Required("html_url"): Url(),
    Required("labels_url"): Url(),
    Required("id"): int,
    Required("number"): int,
    Required("state"): Schema(Any(*State.all_values())),
    Required("title"): str,
    Required("description"): Schema(Any(str, None)),
    Required("creator"): USER_SCHEMA,
    Required("open_issues"): int,
    Required("closed_issues"): int,
    Required("created_at"): str,
    Required("updated_at"): Schema(Any(str, None)),
    Required("closed_at"): Schema(Any(str, None)),
    Required("due_on"): Schema(Any(str, None))
})

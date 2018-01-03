"""Issue label schema."""

from voluptuous import Schema
from voluptuous import Url

# pylint: disable=no-value-for-parameter


LABEL_SCHEMA = Schema({
    "id": int,
    "url": Url(),
    "name": str,
    "color": str,
    "default": bool
})

"""Utilities for githubcap project."""
import datetime
import json
import logging
import re
import typing

import click

import attr
import daiquiri

_DATETIME_ISO_8601 = "%Y-%m-%dT%H:%M:%SZ"
_PAGINATION_RE = re.compile(r'.*[?!]page=(\d+).*')
_DEFAULT_NO_COLOR_FORMAT = "%(asctime)s [%(process)d] %(levelname)-8.8s %(name)s: %(message)s"
_DEFAULT_COLOR_FORMAT = "%(asctime)s [%(process)d] %(color)s%(levelname)-8.8s %(name)s: %(message)s%(color_stop)s"


def parse_datetime(datetime_string: str) -> datetime.datetime:
    """Parse ISO-8601 datetime representation."""
    return datetime.datetime.strptime(datetime_string, _DATETIME_ISO_8601) if datetime_string is not None else None


def serialize_datetime(datetime_instance: datetime.datetime) -> str:
    """Serialize ISO-8601 datetime representation."""
    return datetime_instance.strftime(_DATETIME_ISO_8601) if datetime_instance is not None else None


def setup_logging(verbose: int, no_color: bool) -> None:
    """Set up logging facilities.

    :param verbose: verbosity level
    :param no_color: do not use color in output
    """
    level = logging.WARNING
    if verbose == 1:
        level = logging.INFO
    elif verbose > 1:
        level = logging.DEBUG

    formatter = daiquiri.formatter.ColorFormatter(fmt=_DEFAULT_COLOR_FORMAT)
    if no_color:
        formatter = logging.Formatter(fmt=_DEFAULT_NO_COLOR_FORMAT)

    daiquiri.setup(level=level, outputs=(
        daiquiri.output.Stream(formatter=formatter),
    ))


def dict2json(dict_: dict, pretty: bool = True) -> str:
    """Convert dict to json (string).

    :param dict_: dictionary to be converted
    :param pretty: if True, nice formatting will be used
    :return: formatted dict in json
    """
    kwargs = {}
    if pretty:
        kwargs['sort_keys'] = True
        kwargs['separators'] = (',', ': ')
        kwargs['indent'] = 2

    return json.dumps(dict_, **kwargs)


def next_pagination_page(headers: dict) -> typing.Optional[int]:
    """Parse next paginated page from HTTP headers.

    :param headers: response headers that were returned by GitHub
    :return: next pagination page or None if no other page remains
    """
    link = headers.get('Link')
    if link is None:
        # If there is no next page, GitHub does not provide 'Link'
        return None

    parts = link.split(',')
    for part in parts:
        if not part.endswith('rel="next"'):
            continue

        matched = _PAGINATION_RE.match(part)
        return int(matched.group(1))

    return None


def print_command_result(result: dict, pretty=True) -> None:
    """Print results.

    :param result: a result to be printed
    :param pretty: print result in a pretty way
    :type pretty: bool
    """
    result = dict2json(result, pretty=pretty)
    click.echo("{!s}".format(result))


def get_attr_type(class_: type, attr_name: str) -> type:
    """Get type of attribute in a attr class."""
    return getattr(attr.fields(class_), attr_name).type


def get_option_choices(class_: type, attr_name: str) -> typing.List[str]:
    """Get all choices for an enum."""
    return get_attr_type(class_, attr_name).all_names()


def parse_cli_headers(text_headers: str) -> typing.Dict[str, str]:
    """Parse headers supplied from command line.

    :param text_headers: headers supplied as a text
    :type text_headers: str
    :return: a dictionary representation of headers
    :rtype: dict
    """
    headers = {}
    for header in text_headers.split(','):
        parts = header.split(':', maxsplit=1)
        if len(parts) != 2:
            raise ValueError("Unknown header supplied {!r}, headers should be set as key:value".format(header))

        headers[parts[0]] = parts[1]

    return headers


def command_choice_callback(enum: type, _, param, value) -> type:  # pylint: disable=unused-argument
    """Translate the given value to enum representation."""
    if value is None:
        return None
    return getattr(enum, value)

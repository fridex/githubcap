#!/usr/bin/env python3
"""Implementation of CLI."""

import logging
import sys

import click

import attr
from githubcap import __version__ as githubcap_version
from githubcap import Configuration
import githubcap.commands as cli_commands
from githubcap.utils import parse_cli_headers
from githubcap.utils import setup_logging

# pylint: disable=too-many-arguments

_LOG = logging.getLogger(__name__)


def _print_version(ctx, _, value):
    """Print version information and exit."""
    if not value or ctx.resilient_parsing:
        return

    click.echo("{!s}".format(githubcap_version))
    ctx.exit()


@click.group()
@click.pass_context
@click.option('-v', '--verbose', count=True,
              help="Be verbose about what's going on (can be supplied multiple times).")
@click.option('--version', is_flag=True, is_eager=True, callback=_print_version, expose_value=False,
              help="Print githubcap version and exit.")
@click.option('--no-color', '-C', is_flag=True,
              help="Suppress colorized logging output.")
@click.option('-u', '--user', type=str, envvar='GITHUB_USER', metavar='GITHUB_USER',
              help="GitHub user name.")
@click.option('-p', '--password', type=str, envvar='GITHUB_PASSWORD', metavar='GITHUB_PASSWORD',
              help="GitHub password.")
@click.option('-t', '--token', type=str, envvar='GITHUB_TOKEN', metavar='TOKEN',
              help="Github OAuth2 token.")
@click.option('-R', '--no-omit-rate-limiting', is_flag=True,
              help="Do not omit rate limiting - raise an exception if rate limit exceeds.")
@click.option('-P', '--no-pagination', is_flag=True,
              help="Respect pagination - perform multiple API calls on paginated response.")
@click.option('-H', '--headers', type=str, metavar='KEY1:VAL1,KEY2:VAL2,..',
              help="A comma separated list of headers to be sent.")
@click.option('-l', '--per_page_listing', type=int,
              help="Number of entries in page listing in a single API call.")
@click.option('--github-api', type=str, metavar='URL',
              help="GitHub API endpoint.")
@click.option('--no-validate-schemas', '-S', is_flag=True,
              help="Do not validate schemas from API response.")
@click.option('--config', '-c', type=str, metavar='CONFIG.yaml',
              help="A path to configuration file.")
def cli(ctx=None, verbose=0, no_color=True, user=None, password=None, token=None, config=None,
        no_validate_schemas=False, no_omit_rate_limiting=False, no_pagination=False, headers=None,
        per_page_listing=None, github_api=None):
    """Githubcap command line interface."""
    if ctx:
        ctx.auto_envvar_prefix = 'GITHUBCAP'

    setup_logging(verbose, no_color)

    if config is not None:
        Configuration(config_file=config)

    if user is not None:
        Configuration().user = user
    if password is not None:
        Configuration().password = password
    if token is not None:
        Configuration().token = token
    if per_page_listing is not None:
        Configuration().per_page_listing = per_page_listing
    if github_api is not None:
        Configuration().github_api = github_api
    if headers is not None:
        Configuration().headers = parse_cli_headers(headers)

    Configuration().omit_rate_limiting = not no_omit_rate_limiting
    Configuration().pagination = not no_pagination
    Configuration().validate_schemas = not no_validate_schemas
    _LOG.debug("Configuration: %s", attr.asdict(Configuration().instance))
    _LOG.debug("Supplied cli options: %s", ctx.params)


# Add implemented sub-comands.
for command in cli_commands.__dict__.values():
    if isinstance(command, click.core.Command):
        cli.add_command(command)

if __name__ == '__main__':
    sys.exit(cli())

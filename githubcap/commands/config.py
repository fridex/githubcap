"""Implementation of CLI for configuration file manipulation."""

import logging

import click

from githubcap import Configuration
from githubcap.utils import print_command_result

# pylint: disable=too-many-arguments

_LOG = logging.getLogger(__name__)


@click.command('config')
@click.pass_context
@click.option('--no-pretty', is_flag=True,
              help="Print config in a well formatted manner.")
@click.option('--create', is_flag=True,
              help="Create githubcap configuration file, with default configuration "
                   "options (if not not options not explicitly supplied).")
@click.option('--path', type=str, metavar='CONFIG.yaml',
              help="Write configuration to a config file.")
@click.option('--no-print', '-P', is_flag=True,
              help="Do not print configuration entries to standard output.")
@click.option('--overwrite', '-y', is_flag=True,
              help="Create githubcap configuration file, with default configuration "
                   "options (if not not options not explicitly supplied).")
def cli_config(ctx, no_pretty=False, create=False, overwrite=False, path=None, no_print=False):
    """Manipulate with githubcap configuration."""
    if no_print and not create:
        _LOG.error("Nothing to do, exiting...")
        ctx.exit(1)

    if create:
        Configuration().write2file(path, overwrite=overwrite)

    if not no_print:
        print_command_result(Configuration().to_dict(), pretty=not no_pretty)

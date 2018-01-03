import click

from githubcap.utils import print_command_result
from githubcap.scraping import scrape

# pylint: disable=too-many-arguments


@click.command('scrape')
@click.option('--no-pretty', is_flag=True,
              help="Print results in a well formatted manner.")
@click.option('--resources-dir', '-r', type=str, default='./scraped/resources', show_default=True,
              metavar='RESOURCES_DIR',
              help="A path to a directory where resources should be created.")
@click.option('--schemas-dir', '-s', type=str, default='./scraped/schemas', show_default=True,
              metavar='SCHEMAS_DIR',
              help="A path to a directory where schemas should be created.")
def cli_scrape(no_pretty=False, resources_dir=None, schemas_dir=None):
    result = scrape(resources_dir, schemas_dir)
    print_command_result(result, not no_pretty)

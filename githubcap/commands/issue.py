"""Implementation of CLI for issue manipulation."""

from functools import partial
import logging

import click

from githubcap.resources import IssueHandler
from githubcap.resources import IssuesHandler
from githubcap.utils import command_choice_callback
from githubcap.utils import get_attr_type
from githubcap.utils import get_option_choices
from githubcap.utils import print_command_result

_ISSUES = IssuesHandler()


@click.command('issues')
@click.option('--no-pretty', is_flag=True,
              help="Print results in a well formatted manner.")
@click.option('--organization', '-o', type=str, default=None, metavar='ORGANIZATION',
              help="GitHub owner - GitHub user name or organization name.")
@click.option('--project', '-p', type=str, default=None, metavar='PROJECT_NAME',
              help="GitHub project name.")
@click.option('--page', default=_ISSUES.page, show_default=True,
              help="Page in paginating to start with.")
@click.option('--filter', '-f', default=_ISSUES.filter.name,
              type=click.Choice(get_option_choices(IssuesHandler, 'filter')),
              callback=partial(command_choice_callback, get_attr_type(IssuesHandler, 'filter')), show_default=True,
              help="Filter issues based on assigned state.")
@click.option('--state', '-s', default=_ISSUES.state.name,
              type=click.Choice(get_option_choices(IssuesHandler, 'state')),
              callback=partial(command_choice_callback, get_attr_type(IssuesHandler, 'state')), show_default=True,
              help="Filter issues based on issue state.")
@click.option('--labels', default=_ISSUES.labels, type=str, show_default=True,
              help="Filter issues based on labels - a comma separated list.")
@click.option('--sort', default=_ISSUES.sort.name, type=click.Choice(get_option_choices(IssuesHandler, 'sort')),
              callback=partial(command_choice_callback, get_attr_type(IssuesHandler, 'sort')), show_default=True,
              help="Sorting criteria.")
@click.option('--direction', default=_ISSUES.direction.name,
              type=click.Choice(get_option_choices(IssuesHandler, 'direction')),
              callback=partial(command_choice_callback, get_attr_type(IssuesHandler, 'direction')), show_default=True,
              help="Sorting direction.")
@click.option('--since', default=_ISSUES.since, type=str, show_default=True,
              help="List issues updated at or after the given time.")
@click.option('--milestone', '-m', default=_ISSUES.milestone, type=str, show_default=True,
              help="List issues with the given milestone.")
@click.option('--assignee', '-a', default=_ISSUES.assignee, type=str, metavar="USER", show_default=True,
              help="Filter issues based on assignee.")
@click.option('--creator', '-c', default=_ISSUES.creator, type=str, metavar="USER", show_default=True,
              help="Filter issues based on creator.")
@click.option('--mentioned', '-m', default=_ISSUES.mentioned, type=str, metavar="USER", show_default=True,
              help="Filter issues based on mentioned user.")
def cli_issues(organization=None, project=None, no_pretty=False, **issues_attributes):
    """List GitHub issues."""
    issues = IssuesHandler(**issues_attributes)

    # TODO: split to two commands
    if project is None:
        reported_issues = issues.list_assigned_issues(organization)
    else:
        reported_issues = issues.list_issues(organization, project)
    print_command_result(list(map(lambda x: x.to_dict(), reported_issues)), not no_pretty)


@click.command('issue')
@click.option('--no-pretty', is_flag=True,
              help="Print results in a well formatted manner.")
@click.option('--organization', '-o', type=str, default=None, metavar='ORGANIZATION', required=True,
              help="GitHub owner - GitHub user name or organization name.")
@click.option('--project', '-p', type=str, default=None, metavar='PROJECT_NAME', required=True,
              help="GitHub project name.")
@click.option('--number', '-n', type=int, metavar='ID', required=True,
              help="Issue number (issue identifier).")
def cli_issue(no_pretty=False, organization=None, project=None, number=None):
    """Retrieve a GitHub issue."""
    issue = IssueHandler.by_number(organization, project, number)
    print_command_result(issue.to_dict(), not no_pretty)


@click.command('issue-edit')
@click.option('--no-pretty', is_flag=True,
              help="Print results in a well formatted manner.")
@click.option('--organization', '-o', type=str, default=None, metavar='ORGANIZATION', required=True,
              help="GitHub owner - GitHub user name or organization name.")
@click.option('--project', '-p', type=str, default=None, metavar='PROJECT_NAME', required=True,
              help="GitHub project name.")
@click.option('--number', '-i', type=int, metavar='ID', required=True,
              help="Issue number (issue identifier).")
@click.option('--title', '-t', type=str, metavar='TITLE',
              help="")
@click.option('--body', '-b', type=str, metavar='DESCRIPTION',
              help="")
@click.option('--milestone', '-m', type=str, metavar='MILESTONE_ID',
              help="")
@click.option('--labels', '-l', type=str, metavar='LABEL1,LABEL2,..',
              help="")
@click.option('--assignees', '-a', type=str, metavar='USER1,USER2,..',
              help="")
@click.option('--state', '-s', default=None, type=click.Choice(get_option_choices(IssuesHandler, 'state')),
              callback=partial(command_choice_callback, get_attr_type(IssuesHandler, 'state')), show_default=True,
              help="Filter issues based on issue state.")
def cli_issue_edit(no_pretty=False, organization=None, project=None, number=None, **issue_attributes):
    """Modify a GitHub issue."""
    if all(val is None for val in issue_attributes.values()):
        raise ValueError("No attributes to edit")

    issue = IssueHandler(**issue_attributes).edit(organization, project, number)
    print_command_result(issue.to_dict(), not no_pretty)


@click.command('issue-create')
@click.option('--no-pretty', is_flag=True,
              help="Print results in a well formatted manner.")
@click.option('--organization', '-o', type=str, default=None, metavar='ORGANIZATION', required=True,
              help="GitHub owner - GitHub user name or organization name.")
@click.option('--project', '-p', type=str, default=None, metavar='PROJECT_NAME', required=True,
              help="GitHub project name.")
@click.option('--title', '-t', type=str, metavar='TITLE', required=True,
              help="")
@click.option('--body', '-b', type=str, metavar='DESCRIPTION',
              help="")
@click.option('--milestone', '-m', type=str, metavar='MILESTONE_ID',
              help="")
@click.option('--labels', '-l', type=str, metavar='LABEL1,LABEL2,..',
              help="")
@click.option('--assignees', '-a', type=str, metavar='USER1,USER2,..',
              help="")
@click.option('--state', '-s', default=None, type=click.Choice(get_option_choices(IssuesHandler, 'state')),
              callback=partial(command_choice_callback, get_attr_type(IssuesHandler, 'state')), show_default=True,
              help="Filter issues based on issue state.")
def cli_issue_create(no_pretty=False, organization=None, project=None, **issue_attributes):
    """Create a GitHub issue."""
    issue = IssueHandler(**issue_attributes).create(organization, project)
    print_command_result(issue.to_dict(), not no_pretty)

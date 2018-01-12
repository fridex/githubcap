"""Implementation of CLI for issue manipulation."""

from functools import partial

import click

import githubcap.enums as enums
from githubcap.classes import Issue
from githubcap.utils import command_choice_callback
from githubcap.utils import print_command_result
from githubcap.exceptions import UserInputError


@click.command('issues')
@click.option('--no-pretty', is_flag=True,
              help="Print results in a well formatted manner.")
@click.option('--organization', '-o', type=str, default=None, metavar='ORGANIZATION',
              help="GitHub owner - GitHub user name or organization name.")
@click.option('--project', '-p', type=str, default=None, metavar='PROJECT_NAME',
              help="GitHub project name.")
@click.option('--page', default=0, show_default=True,
              help="Page in paginating to start with.")
@click.option('--filter', '-f', default=enums.Filtering.get_default().name,
              type=click.Choice(enums.Filtering.all_names()),
              callback=partial(command_choice_callback, enums.Filtering), show_default=True,
              help="Filter issues based on assigned state.")
@click.option('--state', '-s', default=enums.IssueState.get_default().name,
              type=click.Choice(enums.IssueState.all_names()),
              callback=partial(command_choice_callback, enums.IssueState), show_default=True,
              help="Filter issues based on issue state.")
@click.option('--labels', default=None, type=str, show_default=True,
              help="Filter issues based on labels - a comma separated list.")
@click.option('--sort', default=enums.Sorting.get_default().name, type=click.Choice(enums.Sorting.all_names()),
              callback=partial(command_choice_callback, enums.Sorting), show_default=True,
              help="Sorting criteria.")
@click.option('--direction', default=enums.SortingDirection.get_default().name,
              type=click.Choice(enums.SortingDirection.all_names()),
              callback=partial(command_choice_callback, enums.SortingDirection), show_default=True,
              help="Sorting direction.")
@click.option('--since', default=None, type=str, show_default=True,
              help="List issues updated at or after the given time.")
@click.option('--milestone', '-m', default=None, type=str, show_default=True,
              help="List issues with the given milestone.")
@click.option('--assignee', '-a', default=None, type=str, metavar="USER",
              help="Filter issues based on assignee.")
@click.option('--creator', '-c', default=None, type=str, metavar="USER",
              help="Filter issues based on creator.")
@click.option('--mentioned', '-m', default=None, type=str, metavar="USER",
              help="Filter issues based on mentioned user.")
def cli_issues(organization=None, project=None, no_pretty=False, **issues_query):
    """List GitHub issues."""
    if organization is None and project is None:
        reported_issues = Issue.list_assigned_issues(**issues_query)
    elif organization is not None and project is None:
        reported_issues = Issue.list_organization_issues(organization, **issues_query)
    elif organization is not None and project is not None:
        reported_issues = Issue.list_project_issues(organization, project, **issues_query)
    else:
        raise UserInputError("Organization has to be specified explicitly for project %r" % project)

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
    issue = Issue.by_number(organization, project, number)
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
@click.option('--state', '-s', default=None, type=click.Choice(enums.IssueState.all_names()),
              callback=partial(command_choice_callback, enums.IssueState), show_default=True,
              help="Filter issues based on issue state.")
def cli_issue_edit(no_pretty=False, organization=None, project=None, number=None, **issue_attributes):
    """Modify a GitHub issue."""
    if all(val is None for val in issue_attributes.values()):
        raise UserInputError("No attributes to edit")

    # TODO: edit by number
    issue = Issue.edit(organization, project, number, issue_attributes)
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
@click.option('--state', '-s', default=None, type=click.Choice(enums.IssueState.all_names()),
              callback=partial(command_choice_callback, enums.IssueState), show_default=True,
              help="Filter issues based on issue state.")
def cli_issue_create(no_pretty=False, organization=None, project=None, **issue_attributes):
    """Create a GitHub issue."""
    issue = Issue.from_dict(**issue_attributes)
    issue = issue.create(organization, project)
    print_command_result(issue.to_dict(), not no_pretty)

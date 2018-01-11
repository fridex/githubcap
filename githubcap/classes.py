from datetime import datetime
import typing

import attr
from voluptuous import Schema

from githubcap.base import GitHubBase
import githubcap.enums as enums
import githubcap.schemas as schemas


@attr.s
class User(GitHubBase):
    """A GitHub user."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.USER_SCHEMA

    avatar_url = attr.ib(type=str)
    events_url = attr.ib(type=str)
    followers_url = attr.ib(type=str)
    following_url = attr.ib(type=str)
    gists_url = attr.ib(type=str)
    gravatar_id = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    login = attr.ib(type=str)
    organizations_url = attr.ib(type=str)
    received_events_url = attr.ib(type=str)
    repos_url = attr.ib(type=str)
    site_admin = attr.ib(type=bool)
    starred_url = attr.ib(type=str)
    subscriptions_url = attr.ib(type=str)
    type = attr.ib(type=enums.UserType)
    url = attr.ib(type=str)

    bio = attr.ib(type=str, default=None)
    blog = attr.ib(type=str, default=None)
    company = attr.ib(type=str, default=None)
    created_at = attr.ib(type=datetime, default=None)
    email = attr.ib(type=str, default=None)
    followers = attr.ib(type=int, default=None)
    following = attr.ib(type=int, default=None)
    hireable = attr.ib(type=bool, default=None)
    location = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    public_gists = attr.ib(type=int, default=None)
    public_repos = attr.ib(type=int, default=None)
    updated_at = attr.ib(type=datetime, default=None)


@attr.s
class RepositoryPermissions(GitHubBase):
    """Permissions for a repository."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.REPOSITORY_PERMISSIONS_SCHEMA

    admin = attr.ib(type=bool)
    pull = attr.ib(type=bool)
    push = attr.ib(type=bool)


@attr.s
class Organization(GitHubBase):
    """A GitHub organization."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.ORGANIZATION_SCHEMA

    avatar_url = attr.ib(type=str)
    description = attr.ib(type=str)
    events_url = attr.ib(type=str)
    hooks_url = attr.ib(type=str)
    id = attr.ib(type=int)
    issues_url = attr.ib(type=str)
    login = attr.ib(type=str)
    members_url = attr.ib(type=str)
    public_members_url = attr.ib(type=str)
    repos_url = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class License(GitHubBase):
    """License definition."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.LICENSE_SCHEMA

    key = attr.ib(type=str)
    name = attr.ib(type=str)
    spdx_id = attr.ib(type=typing.Union[str, None])
    url = attr.ib(type=str)


@attr.s
class Repository(GitHubBase):
    """A repository definition."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.REPOSITORY_SCHEMA

    archived = attr.ib(type=bool)
    archive_url = attr.ib(type=str)
    assignees_url = attr.ib(type=str)
    blobs_url = attr.ib(type=str)
    branches_url = attr.ib(type=str)
    clone_url = attr.ib(type=str)
    collaborators_url = attr.ib(type=str)
    comments_url = attr.ib(type=str)
    commits_url = attr.ib(type=str)
    compare_url = attr.ib(type=str)
    contents_url = attr.ib(type=str)
    contributors_url = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    default_branch = attr.ib(type=str)
    deployments_url = attr.ib(type=str)
    description = attr.ib(type=typing.Union[str, None])
    downloads_url = attr.ib(type=str)
    events_url = attr.ib(type=str)
    fork = attr.ib(type=bool)
    forks = attr.ib(type=int)
    forks_count = attr.ib(type=int)
    forks_url = attr.ib(type=str)
    full_name = attr.ib(type=str)
    git_commits_url = attr.ib(type=str)
    git_refs_url = attr.ib(type=str)
    git_tags_url = attr.ib(type=str)
    git_url = attr.ib(type=str)
    has_downloads = attr.ib(type=bool)
    has_issues = attr.ib(type=bool)
    has_pages = attr.ib(type=bool)
    has_projects = attr.ib(type=bool)
    has_wiki = attr.ib(type=bool)
    homepage = attr.ib(type=typing.Union[str, None])
    hooks_url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    issue_comment_url = attr.ib(type=str)
    issue_events_url = attr.ib(type=str)
    issues_url = attr.ib(type=str)
    keys_url = attr.ib(type=str)
    labels_url = attr.ib(type=str)
    language = attr.ib(type=typing.Union[str, None])
    languages_url = attr.ib(type=str)
    license = attr.ib(type=typing.Union[str, None])
    merges_url = attr.ib(type=str)
    milestones_url = attr.ib(type=str)
    mirror_url = attr.ib(type=str)
    name = attr.ib(type=str)
    notifications_url = attr.ib(type=str)
    open_issues = attr.ib(type=int)
    open_issues_count = attr.ib(type=int)
    owner = attr.ib(type=User)
    private = attr.ib(type=bool)
    pulls_url = attr.ib(type=str)
    pushed_at = attr.ib(type=datetime)
    releases_url = attr.ib(type=str)
    size = attr.ib(type=int)
    ssh_url = attr.ib(type=str)
    stargazers_count = attr.ib(type=int)
    stargazers_url = attr.ib(type=str)
    statuses_url = attr.ib(type=str)
    subscribers_url = attr.ib(type=str)
    subscription_url = attr.ib(type=str)
    svn_url = attr.ib(type=str)
    tags_url = attr.ib(type=str)
    teams_url = attr.ib(type=str)
    trees_url = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    watchers = attr.ib(type=int)
    watchers_count = attr.ib(type=int)

    allow_merge_commit = attr.ib(type=bool, default=None)
    allow_rebase_merge = attr.ib(type=bool, default=None)
    allow_squash_merge = attr.ib(type=bool, default=None)
    network_count = attr.ib(type=int, default=None)
    permissions = attr.ib(type=RepositoryPermissions, default=None)
    subscribers_count = attr.ib(type=int, default=None)
    topics = attr.ib(type=typing.List[str], default=None)


@attr.s
class App(GitHubBase):
    """GitHub application."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.APP_SCHEMA

    client_id = attr.ib(type=str)
    name = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class Authorization(GitHubBase):
    """Authorization definition."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.AUTHORIZATION_SCHEMA

    app = attr.ib(type=App)
    created_at = attr.ib(type=datetime)
    fingerprint = attr.ib(type=str)
    hashed_token = attr.ib(type=str)
    id = attr.ib(type=int)
    note = attr.ib(type=str)
    note_url = attr.ib(type=str)
    scopes = attr.ib(type=enums.AuthorizationScope)
    token = attr.ib(type=str)
    token_last_eight = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)


@attr.s
class AuthorizationInfo(GitHubBase):
    """Authorization information."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.AUTHORIZATION_INFO_SCHEMA

    app = attr.ib(type=App)
    created_at = attr.ib(type=datetime)
    fingerprint = attr.ib(type=str)
    hashed_token = attr.ib(type=str)
    id = attr.ib(type=int)
    note = attr.ib(type=str)
    note_url = attr.ib(type=str)
    scopes = attr.ib(type=enums.AuthorizationScope)
    token = attr.ib(type=str)
    token_last_eight = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class ThreadSubscription(GitHubBase):
    """Subscription to a thread."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.THREAD_SUBSCRIPTION_SCHEMA

    created_at = attr.ib(type=datetime)
    ignored = attr.ib(type=bool)
    reason = attr.ib(type=typing.Union[str, None])
    subscribed = attr.ib(type=bool)
    thread_url = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class GistFork(GitHubBase):
    """Fork of a gist."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIST_FORK_SCHEMA

    created_at = attr.ib(type=datetime)
    id = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class GistHistory(GitHubBase):
    """Gist history representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIST_HISTORY_SCHEMA

    change_status = attr.ib(type=dict)
    committed_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)
    version = attr.ib(type=str)


@attr.s
class Gist(GitHubBase):
    """A GitHub gist."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIST_SCHEMA

    comments = attr.ib(type=int)
    comments_url = attr.ib(type=str)
    commits_url = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    description = attr.ib(type=str)
    files = attr.ib(type=dict)
    forks = attr.ib(type=typing.List[GistFork])
    forks_url = attr.ib(type=str)
    git_pull_url = attr.ib(type=str)
    git_push_url = attr.ib(type=str)
    history = attr.ib(type=typing.List[GistHistory])
    html_url = attr.ib(type=str)
    id = attr.ib(type=str)
    owner = attr.ib(type=User)
    public = attr.ib(type=bool)
    truncated = attr.ib(type=bool)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class GistComment(GitHubBase):
    """A comment to a gist."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIST_COMMENT_SCHEMA

    body = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    id = attr.ib(type=int)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class CommitRef(GitHubBase):
    """A commit ref."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.COMMIT_REF_SCHEMA

    sha = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class CommitPersonInfo(GitHubBase):
    """Information about a person (committer or author) of a commit."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.COMMIT_PERSON_INFO_SCHEMA

    date = attr.ib(type=str)
    email = attr.ib(type=str)
    name = attr.ib(type=str)


@attr.s
class Commit(GitHubBase):
    """A commit representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.COMMIT_SCHEMA

    author = attr.ib(type=User)
    committer = attr.ib(type=CommitPersonInfo)
    message = attr.ib(type=str)
    parents = attr.ib(type=typing.List[CommitRef])
    sha = attr.ib(type=str)
    tree = attr.ib(type=CommitRef)
    url = attr.ib(type=str)
    verification = attr.ib(type=dict)


@attr.s
class GitObject(GitHubBase):
    """Git object representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIT_OBJECT_SCHEMA

    sha = attr.ib(type=str)
    type = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class GitRef(GitHubBase):
    """A git ref."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIT_REF_SCHEMA

    object = attr.ib(type=GitObject)
    ref = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class GitVerification(GitHubBase):
    """Git verification entry."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIT_VERIFICATION_SCHEMA

    payload = attr.ib(type=object)
    reason = attr.ib(type=str)
    signature = attr.ib(type=object)
    verified = attr.ib(type=bool)


@attr.s
class GitTag(GitHubBase):
    """A tag in Git."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIT_TAG_SCHEMA

    message = attr.ib(type=str)
    object = attr.ib(type=GitObject)
    sha = attr.ib(type=str)
    tag = attr.ib(type=str)
    tagger = attr.ib(type=User)
    url = attr.ib(type=str)
    verification = attr.ib(type=GitVerification)


@attr.s
class GitTreeStructure(GitHubBase):
    """"Git tree structure."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIT_TREE_STRUCTURE_SCHEMA

    mode = attr.ib(type=int)
    path = attr.ib(type=str)
    sha = attr.ib(type=str)
    type = attr.ib(type=str)

    size = attr.ib(type=int, default=None)
    url = attr.ib(type=str, default=None)


@attr.s
class GitTree(GitHubBase):
    """Git tree."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GIT_TREE_SCHEMA

    sha = attr.ib(type=str)
    tree = attr.ib(type=typing.List[GitTreeStructure])
    truncated = attr.ib(type=bool)
    url = attr.ib(type=str)


@attr.s
class GithubApp(GitHubBase):
    """GitHub application."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GITHUB_APP_SCHEMA

    created_at = attr.ib(type=datetime)
    description = attr.ib(type=str)
    external_url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    name = attr.ib(type=str)
    owner = attr.ib(type=User)
    updated_at = attr.ib(type=datetime)


@attr.s
class RepositoriesListing(GitHubBase):
    """A listing of repositories."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.REPOSITORIES_LISTING_SCHEMA

    repositories = attr.ib(type=typing.List[Repository])
    total_count = attr.ib(type=int)


@attr.s
class IssueComment(GitHubBase):
    """A comment to an issue."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.ISSUE_COMMENT_SCHEMA

    body = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class Label(GitHubBase):
    """GitHub label."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.LABEL_SCHEMA

    color = attr.ib(type=str)
    default = attr.ib(type=bool)
    id = attr.ib(type=int)
    name = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class Milestone(GitHubBase):
    """A milestone on GitHub."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.MILESTONE_SCHEMA

    closed_at = attr.ib(type=typing.Union[datetime, None])
    closed_issues = attr.ib(type=int)
    created_at = attr.ib(type=datetime)
    creator = attr.ib(type=User)
    description = attr.ib(type=typing.Union[str, None])
    due_on = attr.ib(type=typing.Union[str, None])
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    labels_url = attr.ib(type=str)
    number = attr.ib(type=int)
    open_issues = attr.ib(type=int)
    state = attr.ib(type=str)
    title = attr.ib(type=str)
    updated_at = attr.ib(type=typing.Union[datetime, None])
    url = attr.ib(type=str)


@attr.s
class Migration(GitHubBase):
    """GitHub migration."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.MIGRATION_SCHEMA

    created_at = attr.ib(type=datetime)
    exclude_attachments = attr.ib(type=bool)
    guid = attr.ib(type=str)
    id = attr.ib(type=int)
    lock_repositories = attr.ib(type=bool)
    repositories = attr.ib(type=typing.List[Repository])
    state = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)


@attr.s
class SourceImport(GitHubBase):
    """Source importing."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.SOURCE_IMPORT_SCHEMA

    authors_count = attr.ib(type=int)
    authors_url = attr.ib(type=str)
    commit_count = attr.ib(type=int)
    has_large_files = attr.ib(type=bool)
    html_url = attr.ib(type=str)
    large_files_count = attr.ib(type=int)
    large_files_size = attr.ib(type=int)
    percent = attr.ib(type=int)
    repository_url = attr.ib(type=str)
    status = attr.ib(type=str)
    status_text = attr.ib(type=str)
    url = attr.ib(type=str)
    use_lfs = attr.ib(type=str)
    vcs = attr.ib(type=str)
    vcs_url = attr.ib(type=str)


@attr.s
class CodeOfConduct(GitHubBase):
    """Code of conduct on GitHub."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.CODE_OF_CONDUCT_SCHEMA

    body = attr.ib(type=str)
    key = attr.ib(type=str)
    name = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class OrganizationMembership(GitHubBase):
    """Membership to an organization."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.ORGANIZATION_MEMBERSHIP_SCHEMA

    organization = attr.ib(type=Organization)
    organization_url = attr.ib(type=str)
    role = attr.ib(type=enums.OrganizationRole)
    state = attr.ib(type=enums.OrganizationState)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class ErrorReport(GitHubBase):
    """An error report."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.ERROR_REPORT_SCHEMA

    message = attr.ib(type=str)

    documentation_url = attr.ib(type=str, default=None)


@attr.s
class ErrorTeam(GitHubBase):
    """An error reported with teams."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.ERROR_TEAM_SCHEMA

    errors = attr.ib(type=typing.List[object])
    message = attr.ib(type=str)


@attr.s
class Hook(GitHubBase):
    """GitHub hook representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.HOOK_SCHEMA

    active = attr.ib(type=bool)
    config = attr.ib(type=dict)
    created_at = attr.ib(type=datetime)
    events = attr.ib(type=typing.List[enums.OrganizationState])  # TODO
    id = attr.ib(type=int)
    name = attr.ib(type=str)
    ping_url = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)

    test_url = attr.ib(type=str, default=None)


@attr.s
class ProjectCard(GitHubBase):
    """GitHub project card."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.PROJECT_CARD_SCHEMA

    column_url = attr.ib(type=str)
    content_url = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    creator = attr.ib(type=User)
    id = attr.ib(type=int)
    note = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)


@attr.s
class ProjectColumn(GitHubBase):
    """GitHub project column."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.PROJECT_COLUMN_SCHEMA

    cards_url = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    id = attr.ib(type=int)
    name = attr.ib(type=str)
    project_url = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)


@attr.s
class Branch(GitHubBase):
    """Git branch info."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.BRANCH_SCHEMA

    label = attr.ib(type=str)
    ref = attr.ib(type=str)
    repo = attr.ib(type=Repository)
    sha = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class PullRequest(GitHubBase):
    """A pull request representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.PULL_REQUEST_SCHEMA

    assignee = attr.ib(type=User)
    base = attr.ib(type=Branch)
    body = attr.ib(type=str)
    closed_at = attr.ib(type=datetime)
    comments_url = attr.ib(type=str)
    commits_url = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    diff_url = attr.ib(type=str)
    head = attr.ib(type=Branch)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    issue_url = attr.ib(type=str)
    _links = attr.ib(type=dict)
    locked = attr.ib(type=bool)
    merged_at = attr.ib(type=datetime)
    milestone = attr.ib(type=Milestone)
    number = attr.ib(type=int)
    patch_url = attr.ib(type=str)
    review_comments_url = attr.ib(type=str)
    review_comment_url = attr.ib(type=str)
    state = attr.ib(type=str)
    statuses_url = attr.ib(type=str)
    title = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class Review(GitHubBase):
    """A pull request review."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.REVIEW_SCHEMA

    body = attr.ib(type=str)
    commit_id = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    _links = attr.ib(type=dict)
    pull_request_url = attr.ib(type=str)
    state = attr.ib(type=enums.ReviewState)
    user = attr.ib(type=User)


@attr.s
class PullRequestComment(GitHubBase):
    """A pull request comment."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.PULL_REQUEST_COMMENT_SCHEMA

    body = attr.ib(type=str)
    commit_id = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    diff_hunk = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    in_reply_to_id = attr.ib(type=int)
    _links = attr.ib(type=dict)
    original_commit_id = attr.ib(type=str)
    original_position = attr.ib(type=int)
    path = attr.ib(type=str)
    position = attr.ib(type=int)
    pull_request_review_id = attr.ib(type=int)
    pull_request_url = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class CommentReaction(GitHubBase):
    """A comment reaction."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.COMMENT_REACTION_SCHEMA

    content = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    id = attr.ib(type=int)
    user = attr.ib(type=User)


@attr.s
class TopicsListing(GitHubBase):
    """A listing of topics assigned to a repo."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.TOPICS_LISTING_SCHEMA

    names = attr.ib(type=typing.List[str])


@attr.s
class CommitComment(GitHubBase):
    """A comment to a commit."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.COMMIT_COMMENT_SCHEMA

    body = attr.ib(type=str)
    commit_id = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    line = attr.ib(type=int)
    path = attr.ib(type=str)
    position = attr.ib(type=int)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)


@attr.s
class ContentEntry(GitHubBase):
    """A content entry."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.CONTENT_ENTRY_SCHEMA

    download_url = attr.ib(type=str)
    git_url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    _links = attr.ib(type=dict)
    name = attr.ib(type=str)
    path = attr.ib(type=str)
    sha = attr.ib(type=str)
    size = attr.ib(type=int)
    type = attr.ib(type=str)
    url = attr.ib(type=str)


@attr.s
class Content(GitHubBase):
    """GitHub content."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.CONTENT_SCHEMA

    commit = attr.ib(type=Commit)
    content = attr.ib(type=typing.Union[ContentEntry, None])


@attr.s
class Invitation(GitHubBase):
    """GitHub invitation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.INVITATION_SCHEMA

    created_at = attr.ib(type=datetime)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    invitee = attr.ib(type=User)
    inviter = attr.ib(type=User)
    permissions = attr.ib(type=RepositoryPermissions)
    repository = attr.ib(type=Repository)
    url = attr.ib(type=str)


@attr.s
class ReleaseAsset(GitHubBase):
    """Release asset representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.RELEASE_ASSET_SCHEMA

    browser_download_url = attr.ib(type=str)
    content_type = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    download_count = attr.ib(type=int)
    id = attr.ib(type=int)
    label = attr.ib(type=str)
    name = attr.ib(type=str)
    size = attr.ib(type=int)
    updated_at = attr.ib(type=datetime)
    uploader = attr.ib(type=User)
    url = attr.ib(type=str)


@attr.s
class Release(GitHubBase):
    """A project release on GitHub."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.RELEASE_SCHEMA

    assets = attr.ib(type=typing.List[ReleaseAsset])
    assets_url = attr.ib(type=str)
    author = attr.ib(type=User)
    body = attr.ib(type=str)
    browser_download_url = attr.ib(type=str)
    content_type = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    download_count = attr.ib(type=int)
    draft = attr.ib(type=bool)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    label = attr.ib(type=str)
    name = attr.ib(type=str)
    prerelease = attr.ib(type=bool)
    published_at = attr.ib(type=datetime)
    size = attr.ib(type=int)
    state = attr.ib(type=enums.AssetState)
    tag_name = attr.ib(type=str)
    tarball_url = attr.ib(type=str)
    target_commitish = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    uploader = attr.ib(type=User)
    upload_url = attr.ib(type=str)
    url = attr.ib(type=str)
    zipball_url = attr.ib(type=str)


@attr.s
class SearchResult(GitHubBase):
    """A search result (a search entry)."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.SEARCH_RESULT_SCHEMA

    fragment = attr.ib(type=str)
    matches = attr.ib(type=typing.List[dict])
    object_type = attr.ib(type=str)
    object_url = attr.ib(type=str)
    property = attr.ib(type=str)


@attr.s
class SearchResults(GitHubBase):
    """Listing of search results."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.SEARCH_RESULTS_SCHEMA

    text_matches = attr.ib(type=typing.List['SearchResults'])


@attr.s
class GpgKey(GitHubBase):
    """A GPG key representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.GPG_KEY_SCHEMA

    can_certify = attr.ib(type=bool)
    can_encrypt_comms = attr.ib(type=bool)
    can_encrypt_storage = attr.ib(type=bool)
    can_sign = attr.ib(type=bool)
    created_at = attr.ib(type=datetime)
    emails = attr.ib(type=typing.List[dict])
    expires_at = attr.ib(type=typing.Union[datetime, None])
    id = attr.ib(type=int)
    key_id = attr.ib(type=str)
    primary_key_id = attr.ib(type=typing.Union[str, None])
    public_key = attr.ib(type=str)
    subkeys = attr.ib(type=typing.List['GpgKey'])


@attr.s
class Key(GitHubBase):
    """GitHub key representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.KEY_SCHEMA

    created_at = attr.ib(type=datetime)
    id = attr.ib(type=int)
    key = attr.ib(type=str)
    read_only = attr.ib(type=bool)
    title = attr.ib(type=str)
    url = attr.ib(type=str)
    verified = attr.ib(type=bool)


@attr.s
class Issue(GitHubBase):
    """An issue representation."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.ISSUE_SCHEMA

    assignees = attr.ib(type=typing.List[User])
    author_association = attr.ib(type=enums.AuthorAssociation)
    body = attr.ib(type=typing.Union[str, None])
    closed_at = attr.ib(type=typing.Union[datetime, None])
    comments = attr.ib(type=int)
    comments_url = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    events_url = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    labels = attr.ib(type=typing.List[Label])
    labels_url = attr.ib(type=str)
    locked = attr.ib(type=bool)
    milestone = attr.ib(type=Milestone)
    number = attr.ib(type=int)
    repository_url = attr.ib(type=str)
    state = attr.ib(type=enums.IssueState)
    title = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)
    user = attr.ib(type=User)

    assignee = attr.ib(type=User, default=None)
    closed_by = attr.ib(type=User, default=None)
    pull_request = attr.ib(type=dict, default=None)
    repository = attr.ib(type=Repository, default=None)

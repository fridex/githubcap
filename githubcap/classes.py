from datetime import datetime
import typing

import attr
from voluptuous import Schema

import githubcap.enums as enums
import githubcap.schemas as schemas

from .base import GitHubBase
from .exceptions import HTTPError

# Break cyclic type dependencies where needed.
_TeamType = typing.TypeVar('T', bound='Team')
_RepositoryType = typing.TypeVar('T', bound='Repository')
_IssueType = typing.TypeVar('T', bound='Issue')


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

    @classmethod
    def unblock_user_by_name(cls, username: str):
        cls._call('/user/blocks/{username}'.format(username=username), method='DELETE')

    @classmethod
    def remove_emails(cls, emails: typing.List[str]):
        cls._call('/user/emails',payload=emails,  method='DELETE')

    @classmethod
    def get_public_emails(cls) -> typing.List[str]:
        response, _ = cls._call('/user/public_emails', method='GET')
        return response

    @classmethod
    def update(cls, name: str = None, email: str = None, blog: str = None, company: str = None,
               location: str = None, hireable: bool = None, bio: str = None):
        payload = {}

        if name is not None:
            payload['name'] = name
        if email is not None:
            payload['email'] = email
        if blog is not None:
            payload['blog'] = blog
        if company is not None:
            payload['company'] = company
        if location is not None:
            payload['location'] = location
        if hireable is not None:
            payload['hireable'] = hireable
        if bio is not None:
            payload['bio'] = bio

        response, _ = cls._call('/user', payload=payload, method='PATCH')
        return cls.from_response(response)

    def remove_from_organization(self, org: str):
        """"In order to remove a user's membership with an organization.

        The authenticated user must be an organization owner.
        """
        Organization.remove_user_from_organization(org, self.login)

    @classmethod
    def publicize_organization_membership_by_username(cls, org: str, username: str):
        Organization.publicize_user_membership_by_username(org, username)

    @classmethod
    def hide_organization_membership_by_username(cls, org: str, username: str):
        Organization.hide_user_membership_by_username(org, username)


@attr.s
class RepositoryPermissions(GitHubBase):
    """Permissions for a repository."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.REPOSITORY_PERMISSIONS_SCHEMA

    admin = attr.ib(type=bool)
    pull = attr.ib(type=bool)
    push = attr.ib(type=bool)


@attr.s
class Repository(GitHubBase):
    """A repository definition."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.REPOSITORY_SCHEMA

    name = attr.ib(type=str)

    allow_merge_commit = attr.ib(type=bool, default=None)
    allow_rebase_merge = attr.ib(type=bool, default=None)
    allow_squash_merge = attr.ib(type=bool, default=None)
    archived = attr.ib(type=bool, default=None)
    archive_url = attr.ib(type=str, default=None)
    assignees_url = attr.ib(type=str, default=None)
    blobs_url = attr.ib(type=str, default=None)
    branches_url = attr.ib(type=str, default=None)
    clone_url = attr.ib(type=str, default=None)
    collaborators_url = attr.ib(type=str, default=None)
    comments_url = attr.ib(type=str, default=None)
    commits_url = attr.ib(type=str, default=None)
    compare_url = attr.ib(type=str, default=None)
    contents_url = attr.ib(type=str, default=None)
    contributors_url = attr.ib(type=str, default=None)
    created_at = attr.ib(type=datetime, default=None)
    default_branch = attr.ib(type=str, default=None)
    deployments_url = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    downloads_url = attr.ib(type=str, default=None)
    events_url = attr.ib(type=str, default=None)
    fork = attr.ib(type=bool, default=None)
    forks = attr.ib(type=int, default=None)
    forks_count = attr.ib(type=int, default=None)
    forks_url = attr.ib(type=str, default=None)
    full_name = attr.ib(type=str, default=None)
    git_commits_url = attr.ib(type=str, default=None)
    git_refs_url = attr.ib(type=str, default=None)
    git_tags_url = attr.ib(type=str, default=None)
    git_url = attr.ib(type=str, default=None)
    has_downloads = attr.ib(type=bool, default=None)
    has_issues = attr.ib(type=bool, default=None)
    has_pages = attr.ib(type=bool, default=None)
    has_projects = attr.ib(type=bool, default=None)
    has_wiki = attr.ib(type=bool, default=None)
    homepage = attr.ib(type=str, default=None)
    hooks_url = attr.ib(type=str, default=None)
    html_url = attr.ib(type=str, default=None)
    id = attr.ib(type=int, default=None)
    issue_comment_url = attr.ib(type=str, default=None)
    issue_events_url = attr.ib(type=str, default=None)
    issues_url = attr.ib(type=str, default=None)
    keys_url = attr.ib(type=str, default=None)
    labels_url = attr.ib(type=str, default=None)
    language = attr.ib(type=str, default=None)
    languages_url = attr.ib(type=str, default=None)
    license = attr.ib(type=str, default=None)
    merges_url = attr.ib(type=str, default=None)
    milestones_url = attr.ib(type=str, default=None)
    mirror_url = attr.ib(type=str, default=None)
    network_count = attr.ib(type=int, default=None)
    notifications_url = attr.ib(type=str, default=None)
    open_issues = attr.ib(type=int, default=None)
    open_issues_count = attr.ib(type=int, default=None)
    owner = attr.ib(type=User, default=None)
    permissions = attr.ib(type=RepositoryPermissions, default=None)
    private = attr.ib(type=bool, default=None)
    pulls_url = attr.ib(type=str, default=None)
    pushed_at = attr.ib(type=datetime, default=None)
    releases_url = attr.ib(type=str, default=None)
    size = attr.ib(type=int, default=None)
    ssh_url = attr.ib(type=str, default=None)
    stargazers_count = attr.ib(type=int, default=None)
    stargazers_url = attr.ib(type=str, default=None)
    statuses_url = attr.ib(type=str, default=None)
    subscribers_count = attr.ib(type=int, default=None)
    subscribers_url = attr.ib(type=str, default=None)
    subscription_url = attr.ib(type=str, default=None)
    svn_url = attr.ib(type=str, default=None)
    tags_url = attr.ib(type=str, default=None)
    teams_url = attr.ib(type=str, default=None)
    topics = attr.ib(type=typing.List[str], default=None)
    trees_url = attr.ib(type=str, default=None)
    updated_at = attr.ib(type=datetime, default=None)
    url = attr.ib(type=str, default=None)
    watchers = attr.ib(type=int, default=None)
    watchers_count = attr.ib(type=int, default=None)

    def create_in_organization(self, org) -> _RepositoryType:
        """"Create a new repository in an organization.

        The authenticated user must be a member of the specified organization.
        """
        return Organization.create_repository_in_organization(org, self)

    @classmethod
    def delete_repository(cls, owner: str, repo: str):
        """"Deleting a repository requires admin access.  If OAuth is used, the delete_repo scope is required."""
        cls._call('/repos/{owner}/{repo}'.format(owner=owner, repo=repo), method='DELETE')

    def detele(self):
        owner, name = self.full_name.split('/')
        self.delete_repository(owner, name)

    @classmethod
    def check_assignee_by_name(cls, owner: str, repo: str, assignee: str):
        """Checks if a user has permission to be assigned to an issue in this repository."""
        cls._call("repos/{owner}/{repo}/assignees/{assignee}".format(owner=owner, repo=repo, assignee=assignee))

    def check_assignee(self, assignee: str):
        """Checks if a user has permission to be assigned to an issue in this repository."""
        owner, name = self.full_name.split('/')
        return self.check_assignee_by_name(owner, name, assignee)

    @classmethod
    def remove_collaborator_by_name(cls, owner: str, repo: str, username: str):
        response, _ = cls._call('/repos/{owner}/{repo}/collaborators/{username}'
                                .format(owner=owner, username=username, repo=repo), method='DELETE')
        return cls.from_response(response)

    def remove_collaborator(self, username: str):
        owner, name = self.full_name.split('/')
        return self.remove_collaborator_by_name(owner, name, username)

    def get_code_of_conduct(self):
        owner, name = self.full_name.split('/')
        return CodeOfConduct.get_for_repo(owner, name)

    @classmethod
    def delete_file_by_path(cls, owner: str, repo: str, path: str):
        """"This method deletes a file in a repositor."""
        cls._call('/repos/{owner}/{repo}/contents/{path}'.format(owner=owner, path=path, repo=repo), method='DELETE')

    def delete_file(self, path: str):
        owner, repo = self.full_name.split('/')
        return self.delete_file_by_path(owner, repo, path)

    @classmethod
    def fork_by_name(cls, owner: str, repo: str):
        """"Create a fork for the authenticated user."""
        response, _ = cls._call('/repos/{owner}/{repo}/forks'.format(owner=owner, repo=repo), method='POST')
        return cls.from_response(response)

    def fork(self):
        """"Create a fork for the authenticated user."""
        owner, name = self.full_name.split('/')
        return self.fork_by_name(owner, name)

    def get_commit(self, sha: str):
        owner, name = self.full_name.split('/')
        return Commit.get_by_repo(owner, name, sha)

    @classmethod
    def create_issue_in_repo(cls, owner: str, repo: str, issue: _IssueType):
        """"Any user with pull access to a repository can create an issue."""
        response, _ = cls._call('/repos/{owner}/{repo}/issues'
                                .format(owner=owner, repo=repo), payload=issue.to_dict(), method='POST')
        return Issue.from_response(response)

    def create_issue(self, issue: _IssueType):
        """"Any user with pull access to a repository can create an issue."""
        owner, repo = self.full_name.split('/')
        return self.create_issue_in_repo(owner, repo, issue)

    @classmethod
    def get_license_by_name(cls, owner: str, repo: str):
        """"This method returns the contents of the repository's license file, if one is detected."""
        response, _ = cls._call('/repos/{owner}/{repo}/license'.format(owner=owner, repo=repo), method='GET')
        return License.from_response(response)

    def get_license(self):
        owner, name = self.full_name.split('/')
        return self.get_license_by_name(owner, name)

    @classmethod
    def remove_milestone_by_name(cls, owner: str, repo: str,  number: int):
        cls._call('/repos/{owner}/{repo}/milestones/{number}'
                  .format(number=number, owner=owner, repo=repo), method='DELETE')

    def remove_milestone(self, number: int):
        owner, repo = self.full_name.split('/')
        return self.remove_milestone_by_name(owner, repo, number)

    @classmethod
    def get_readme_by_name(cls, owner: str, repo: str):
        """"This method returns the preferred README for a repository."""
        response, _ = cls._call('/repos/{owner}/{repo}/readme'
                                .format(owner=owner, repo=repo), method='GET')
        return response

    def get_readme(self):
        owner, repo = self.full_name.split('/')
        return self.get_readme_by_name(owner, repo)

    @classmethod
    def get_release_by_tag(cls, owner: str, repo: str, tag: str):
        """"Get a published release with the specified tag."""
        response, _ = cls._call('/repos/{owner}/{repo}/releases/tags/{tag}'
                                .format(owner=owner, tag=tag, repo=repo), method='GET')
        return Release.from_response(response)

    def get_release(self, tag: str):
        owner, repo = self.full_name.split('/')
        return self.get_release_by_tag(owner, repo, tag)

    @classmethod
    def delete_release_by_id(cls, owner: str, repo: str, id: int):
        """"Users with push access to the repository can delete a release."""
        response, _ = cls._call('/repos/{owner}/{repo}/releases/{id}'
                                .format(owner=owner, id=id, repo=repo), method='DELETE')
        return cls.from_response(response)

    def delete_release(self, id: int):
        owner, repo = self.full_name.split('/')
        self.delete_release_by_id(owner, repo, id)


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

    @classmethod
    def get_by_name(cls, org: str):
        response, _ = cls._call('/orgs/{org}'.format(org=org), method='PATCH')
        return cls.from_response(response)

    @classmethod
    def remove_user_from_organization(cls, org: str, username: str):
        """"In order to remove a user's membership with an organization.

        The authenticated user must be an organization owner.
        """
        cls._call('/orgs/{org}/memberships/{username}'.format(org=org, username=username), method='DELETE')

    def remove_user(self, username: str):
        """"In order to remove a user's membership with an organization.

        The authenticated user must be an organization owner.
        """
        self.remove_user_from_organization(self.login, username)

    @classmethod
    def publicize_user_membership_by_username(cls, org: str, username: str):
        cls._call('/orgs/{org}/public_members/{username}'.format(org=org, username=username), method='DELETE')

    @classmethod
    def hide_user_membership_by_username(cls, org: str, username: str):
        cls._call('/orgs/{org}/public_members/{username}'.format(org=org, username=username), method='DELETE')

    @classmethod
    def create_repository_in_organization(cls, org: str, repository: Repository) -> Repository:
        """"Create a new repository in a organization.

        The authenticated user must be a member of the specified organization.
        """
        response, _ = cls._call('/orgs/{org}/repos'.format(org=org), payload=repository.as_dict(), method='POST')
        return Repository.from_response(response)

    def create_repository(self, repository: Repository) -> Repository:
        """"Create a new repository in this organization.

        The authenticated user must be a member of the specified organization.
        """
        return self.create_repository_in_organization(self.login, repository)

    @classmethod
    def create_team_in_organization(cls, org: str, team: _TeamType):
        """"To create a team, the authenticated user must be a member of org."""
        return Team.create_in_organization(org, team)

    def create_team(self, team: _TeamType):
        """"To create a team, the authenticated user must be a member of org."""
        return Team.create_in_organization(self.login, team)


@attr.s
class License(GitHubBase):
    """License definition."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.LICENSE_SCHEMA

    key = attr.ib(type=str)
    name = attr.ib(type=str)
    spdx_id = attr.ib(type=str)
    url = attr.ib(type=str)

    @classmethod
    def get_by_name(cls, license: str):
        response, _ = cls._call('/licenses/{license}'.format(license=license), method='GET')
        return cls.from_response(response)


@attr.s
class App(GitHubBase):
    """GitHub application."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.APP_SCHEMA

    client_id = attr.ib(type=str)
    name = attr.ib(type=str)
    url = attr.ib(type=str)

    @classmethod
    def get(cls):
        """"Returns the GitHub App associated with the authentication credentials used."""
        response, _ = cls._call('/app', method='GET')
        return cls.from_response(response)

    @classmethod
    def get_by_app_slug(cls, app_slug: str):
        response, _ = cls._call('/apps/{app_slug}'.format(app_slug=app_slug), method='GET')
        return cls.from_response(response)


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
    reason = attr.ib(type=str)
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

    @classmethod
    def delete_by_id(cls, id: int):
        cls._call('/authorizations/{id}'.format(id=id), method='DELETE')

    def delete(self):
        self.delete_by_id(self.id)

    @classmethod
    def get_by_id(cls, id: int):
        response, _ = cls._call('/gists/{id}'.format(id=id), method='DELETE')
        return cls.from_response(response)

    @classmethod
    def is_starred_by_id(cls, id: int):
        try:
            cls._call('/gists/{id}/star'.format(id=id), method='GET')
            return True
        except HTTPError as exc:
            if exc.status_code == 404:
                return False
            raise

    def is_starred(self):
        try:
            self._call('/gists/{id}/star'.format(id=self.id), method='GET')
            return True
        except HTTPError as exc:
            if exc.status_code == 404:
                return False
            raise

    @classmethod
    def get_by_revision(cls, sha: str, id: int):
        response, _ = cls._call('/gists/{id}/{sha}'.format(sha=sha, id=id), method='GET')
        return cls.from_response(response)


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

    @classmethod
    def get_by_id(cls, id: int, gist_id: int):
        response, _ = cls._call('/gists/{gist_id}/comments/{id}'.format(id=id, gist_id=gist_id), method='DELETE')
        return cls.from_response(response)


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

    @classmethod
    def get_by_repo(cls, owner: str, repo: str, sha: str):
        response, _ = cls._call('/repos/{owner}/{repo}/git/commits/{sha}'
                                .format(sha=sha, owner=owner, repo=repo), method='GET')
        return cls.from_response(response)


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

    @classmethod
    def get_by_sha(cls, owner: str, repo: str, sha: str):
        response, _ = cls._call('/repos/{owner}/{repo}/git/trees/{sha}'
                                .format(sha=sha, owner=owner, repo=repo), method='GET')
        return cls.from_response(response)


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

    def edit_issue(self, number: int, owner: str, repo: str):
        """"Issue owners and users with push access can edit an issue."""
        response, _ = self._call('/repos/{owner}/{repo}/issues/{number}'
                                 .format(number=number, owner=owner, repo=repo),
                                 payload=self.to_dict(), method='PATCH')
        return self.from_response(response)


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

    closed_at = attr.ib(type=datetime)
    closed_issues = attr.ib(type=int)
    created_at = attr.ib(type=datetime)
    creator = attr.ib(type=User)
    description = attr.ib(type=str)
    due_on = attr.ib(type=str)
    html_url = attr.ib(type=str)
    id = attr.ib(type=int)
    labels_url = attr.ib(type=str)
    number = attr.ib(type=int)
    open_issues = attr.ib(type=int)
    state = attr.ib(type=str)
    title = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
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

    @classmethod
    def fetch_status(cls, org: str, id: int):
        """"Fetches the status of a migration."""
        response, _ = cls._call('/orgs/{org}/migrations/{id}'.format(org=org, id=id), method='GET')
        return cls.from_response(response)

    @classmethod
    def delete_migration_archive(cls, org: str, id: int):
        """"Deletes a previous migration archive.

        Migration archives are automatically deleted after seven days.
        """
        cls._call('/orgs/{org}/migrations/{id}/archive'.format(org=org, id=id), method='DELETE')

    @classmethod
    def unlock_repository(cls, org: str, id: int, repo_name: str):
        """"Unlocks a repository that was locked for migration.

        You should unlock each migrated repository and delete them when the migration is complete and
        you no longer need the source data.
        """
        response, _ = cls._call('/orgs/{org}/migrations/{id}/repos/{repo_name}/lock'
                                .format(org=org, id=id, repo_name=repo_name), method='DELETE')
        return cls.from_response(response)


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

    @classmethod
    def stop_import(cls, owner: str, repo: str):
        """"Stop an import for a repository."""
        cls._call('/repos/{owner}/{repo}/import'.format(owner=owner, repo=repo), method='DELETE')


@attr.s
class CodeOfConduct(GitHubBase):
    """Code of conduct on GitHub."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.CODE_OF_CONDUCT_SCHEMA

    body = attr.ib(type=str)
    key = attr.ib(type=str)
    name = attr.ib(type=str)
    url = attr.ib(type=str)

    @classmethod
    def get(cls):
        response, _ = cls._call('/codes_of_conduct', method='GET')
        return cls.from_response(response)
    
    @classmethod
    def get_by_key(cls, key: str):
        response, _ = cls._call('/codes_of_conduct/{key}'.format(key=key), method='GET')
        return cls.from_response(response)

    @classmethod
    def get_for_repo(cls, owner: str, repo: str):
        """"This method returns the contents of the repository's code of conduct file, if one is detected."""
        response, _ = cls._call('/repos/{owner}/{repo}/community/code_of_conduct'
                                .format(owner=owner, repo=repo), method='GET')
        return cls.from_response(response)



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
    events = attr.ib(type=typing.List[enums.OrganizationState])
    id = attr.ib(type=int)
    name = attr.ib(type=str)
    ping_url = attr.ib(type=str)
    updated_at = attr.ib(type=datetime)
    url = attr.ib(type=str)

    test_url = attr.ib(type=str, default=None)

    @classmethod
    def get_by_id(cls, org: str, id: int):
        response, _ = cls._call('/orgs/{org}/hooks/{id}'.format(org=org, id=id), method='DELETE')
        return cls.from_response(response)

    @classmethod
    def ping_hook(cls, org: str, id: int):
        """"This will trigger a ping event to be sent to the hook."""
        response, _ = cls._call('/orgs/{org}/hooks/{id}/pings'.format(org=org, id=id), method='POST')
        return cls.from_response(response)


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

    @classmethod
    def delete_by_id(cls, card_id: int):
        cls._call('/projects/columns/cards/{card_id}'.format(card_id=card_id), method='DELETE')

    def delete(self):
        self.delete_by_id(self.id)

    @classmethod
    def move_by_id(cls, card_id: int, position: int, column_id: int = None):
        payload = {
            'position': position
        }
        if column_id is not None:
            payload['column_id'] = column_id
        response, _ = cls._call('/projects/columns/cards/{card_id}/moves'
                                .format(card_id=card_id), payload=payload, method='POST')
        return response

    def move(self, position: int, column_id: int = None):
        return self.move_by_id(self.id, position, column_id)


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

    @classmethod
    def delete_by_id(cls, column_id: int):
        response, _ = cls._call('/projects/columns/{column_id}'.format(column_id=column_id), method='DELETE')
        return cls.from_response(response)

    def delete(self):
        return self.delete_by_id(self.id)

    @classmethod
    def move_by_id(cls, column_id: int, position: int):
        response, _ = cls._call('/projects/columns/{column_id}/moves'
                                .format(column_id=column_id), payload={'position': position}, method='POST')
        return cls.from_response(response)

    def move(self, position: int):
        return self.move_by_id(self.id, position)


@attr.s
class Project(GitHubBase):

    @classmethod
    def delete_by_id(cls, project_id: int):
        response, _ = cls._call('/projects/{project_id}'.format(project_id=project_id), method='DELETE')
        return response

    def delete(self):
        return self.delete_by_id(self.id)


@attr.s
class Branch(GitHubBase):
    """Git branch info."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.BRANCH_SCHEMA

    label = attr.ib(type=str)
    ref = attr.ib(type=str)
    repo = attr.ib(type=Repository)
    sha = attr.ib(type=str)
    user = attr.ib(type=User)

    @classmethod
    def get_branch_by_name(cls, branch: str, owner: str, repo: str):
        response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}'
                                .format(branch=branch, owner=owner, repo=repo), method='GET')
        return cls.from_response(response)

    @classmethod
    def remove_protection_by_name(cls, branch: str, owner: str, repo: str):
        response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection'
                                .format(branch=branch, owner=owner, repo=repo), method='DELETE')
        # TODO: BranchProtection class


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

    @classmethod
    def remove_by_id(cls, owner: str, repo: str, id: int):
        cls._call('/repos/{owner}/{repo}/pulls/comments/{id}'.format(owner=owner, id=id, repo=repo), method='DELETE')
    

@attr.s
class CommentReaction(GitHubBase):
    """A comment reaction."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.COMMENT_REACTION_SCHEMA

    content = attr.ib(type=str)
    created_at = attr.ib(type=datetime)
    id = attr.ib(type=int)
    user = attr.ib(type=User)

    @classmethod
    def delete_by_id(cls, id: int):
        response, _ = cls._call('/reactions/{id}'.format(id=id), method='DELETE')
        return cls.from_response(response)

    def delete(self):
        return self.delete_by_id(self.id)


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

    @classmethod
    def delete_by_id(cls, owner: str, id: int, repo: str):
        response, _ = cls._call('/repos/{owner}/{repo}/comments/{id}'
                                .format(owner=owner, id=id, repo=repo), method='DELETE')
        return cls.from_response(response)


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
    content = attr.ib(type=ContentEntry)


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
    expires_at = attr.ib(type=datetime)
    id = attr.ib(type=int)
    key_id = attr.ib(type=str)
    primary_key_id = attr.ib(type=str)
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
    body = attr.ib(type=str)
    closed_at = attr.ib(type=datetime)
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

    @classmethod
    def remove_assignees_by_id(cls, owner: str, repo: str, number: int, assignees: typing.List[str]):
        """"Removes one or more assignees from an issue."""
        response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/assignees'
                                .format(number=number, owner=owner, repo=repo),
                                payload={'assignees': assignees}, method='DELETE')
        return cls.from_response(response)

    def remove_assignees(self, assignees: typing.List[str]):
        owner, repo = self.repository.full_name.split('/')
        self.remove_assignees_by_id(owner, repo, self.number, assignees)

    @classmethod
    def remove_label_by_name(cls, owner: str, repo: str, number: int, name: str):
        response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/labels/{name}'
                                .format(number=number, owner=owner, name=name, repo=repo), method='DELETE')
        return cls.from_response(response)

    def remove_label(self, name: str):
        owner, repo = self.repository.full_name.split('/')
        self.remove_label_by_name(owner, repo, self.number, name)

    @classmethod
    def unlock_conversation(cls, owner: str, repo: str, number: int):
        """"Users with push access can unlock an issue's conversation."""
        cls._call('/repos/{owner}/{repo}/issues/{number}/lock'
                  .format(number=number, owner=owner, repo=repo), method='DELETE')

    @classmethod
    def by_number(cls, organization: str, project: str, number: int) -> _IssueType:
        """Retrieve issue based on it's number."""
        uri = '/repos/{org!s}/{project!s}/issues/{number:d}'.format(org=organization, project=project, number=number)
        response, _ = cls._call(uri, method='GET')
        return Issue.from_response(response)

    def create(self, organization: str, project: str) -> _IssueType:
        """Create an issue."""
        uri = '/repos/{org!s}/{project!s}/issues'.format(org=organization, project=project)
        payload = {key: value for key, value in attr.asdict(self).items() if value is not None}
        response, _ = self._call(uri, payload=payload, method='POST')
        return Issue.from_response(response)

    def edit(self, organization: str, project: str, number: int) -> _IssueType:
        """Edit existing issue."""
        uri = '/repos/{org!s}/{project!s}/issues/{number:d}'.format(org=organization, project=project, number=number)
        payload = {key: value for key, value in attr.asdict(self).items() if value is not None}
        response, _ = self._call(uri, payload=payload, method='PATCH')
        # TODO: report not-changed values
        return Issue.from_response(response)


class Team(GitHubBase):
    """Representation of a team."""

    _SCHEMA: typing.ClassVar[Schema] = schemas.TEAM_SCHEMA

    # https://developer.github.com/v3/orgs/teams/#create-team

    name = attr.ib(type=str)

    id = attr.ib(type=int, default=None)
    url = attr.ib(type=str, default=None)
    slug = attr.ib(type=str, default=None)
    description = attr.ib(type=str, default=None)
    privacy = attr.ib(type=enums.TeamPrivacy, default=None)
    permission = attr.ib(type=enums.TeamPermission, default=None)
    members_url = attr.ib(type=str, default=None)
    repositories_url = attr.ib(type=url, default=None)

    members_count = attr.ib(type=int, default=None)
    repos_count = attr.ib(type=int, default=None)
    created_at = attr.ib(type=str, default=None)
    updated_at = attr.ib(type=str, default=None)
    organization = attr.ib(type=Organization, default=None)
    parent = attr.ib(type=_TeamType, default=None)

    @classmethod
    def create_in_organization(cls, org: str, team: _TeamType):
        """"To create a team, the authenticated user must be a member of org."""
        response, _ = cls._call('/orgs/{org}/teams'.format(org=org), payload=team.to_dict(), method='POST')
        return cls.from_response(response)

    @classmethod
    def delete_team_by_id(cls, id: int):
        """"Deleting a parent team will delete all of its child teams as well."""
        cls._call('/teams/{id}'.format(id=id), method='DELETE')

    def delete(self):
        self.delete_team_by_id(self.id)


@attr.s
class Markdown(GitHubBase):
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def render(cls, text: str):
        payload = {
            'text': text,
            'mode': 'markdown'
        }
        response, _ = cls._call('/markdown', payload=payload, method='POST', json_response=False)
        return response


@attr.s
class RateLimit(GitHubBase):
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def get(cls):
        """"Note: Accessing this endpoint does not count against your rate limit."""
        response, _ = cls._call('/rate_limit', method='GET')
        return response

#
# Missing API calls:
#
# @classmethod
# def func_75(cls, branch: str, owner: str, repo: str):
#     """"Removing admin enforcement requires admin access and branch protection to be enabled."""
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/enforce_admins'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
#
# @classmethod
# def func_76(cls, branch: str, owner: str, repo: str):
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
# 
# @classmethod
# def func_77(cls, branch: str, owner: str, repo: str):
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
# 
# @classmethod
# def func_78(cls, branch: str, owner: str, repo: str):
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks/contexts'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
# 
# @classmethod
# def func_79(cls, branch: str, owner: str, repo: str):
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/restrictions'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
# 
# @classmethod
# def func_80(cls, branch: str, owner: str, repo: str):
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
# 
# @classmethod
# def func_81(cls, branch: str, owner: str, repo: str):
#     response, _ = cls._call('/repos/{owner}/{repo}/branches/{branch}/protection/restrictions/users'.format(branch=branch, owner=owner, repo=repo), method='DELETE')
#     return cls.from_response(response)
# 
#
#@classmethod
#def func_2(cls, ):
#    response, _ = cls._call('/app/installations', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_3(cls, installation_id: int):
#    response, _ = cls._call('/app/installations/{installation_id}'.format(installation_id=installation_id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_5(cls, ):
#    """"You can use this API to list the set of OAuth applications that have been granted access to your account. Unlike the list your authorizations API, this API does not manage individual tokens. This API will return one entry for each OAuth application that has been granted access to your account, regardless of the number of tokens an application has generated for your user. The list of OAuth applications returned matches what is shown on the application authorizations settings screen within GitHub. The scopes returned are the union of scopes authorized for the application. For example, if an application has one token with repo scope and another token with user scope, the grant will return ["repo", "user"]."""
#    response, _ = cls._call('/applications/grants', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_5(cls, id: int):
#    """"Deleting an OAuth application's grant will also delete all OAuth tokens associated with the application for your user. Once deleted, the application has no access to your account and is no longer listed on the application authorizations settings screen within GitHub."""
#    response, _ = cls._call('/applications/grants/{id}'.format(id=id), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_6(cls, client_id: int, access_token: str):
#    """"Deleting an OAuth application's grant will also delete all OAuth tokens associated with the application for the user. Once deleted, the application will have no access to the user's account and will no longer be listed on the application authorizations settings screen within GitHub."""
#    response, _ = cls._call('/applications/{client_id}/grants/{access_token}'.format(client_id=client_id, access_token=access_token), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_7(cls, client_id: int, access_token: str):
#    """"OAuth application owners can revoke a single token for an OAuth application. You must use Basic Authentication for this method, where the username is the OAuth application client_id and   the password is its client_secret."""
#    response, _ = cls._call('/applications/{client_id}/tokens/{access_token}'.format(client_id=client_id, access_token=access_token), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_9(cls, ):
#    """"Organizations that enforce SAML SSO require personal access tokens to be whitelisted. Read more about whitelisting tokens on the GitHub Help site."""
#    response, _ = cls._call('/authorizations', method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_10(cls, client_id: int):
#    """"This method will create a new authorization for the specified OAuth application, only if an authorization for that application doesn't already exist for the user. The URL includes the 20 character client ID for the OAuth app that is requesting the token. It returns the user's existing authorization for the application if one is present. Otherwise, it creates and returns a new one."""
#    response, _ = cls._call('/authorizations/clients/{client_id}'.format(client_id=client_id), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_11(cls, fingerprint: str, client_id: int):
#    """"This method will create a new authorization for the specified OAuth application, only if an authorization for that application and fingerprint do not already exist for the user. The URL includes the 20 character client ID for the OAuth app that is requesting the token. fingerprint is a unique string to distinguish an authorization from others created for the same client ID and user. It returns the user's existing authorization for the application if one is present. Otherwise, it creates and returns a new one."""
#    response, _ = cls._call('/authorizations/clients/{client_id}/{fingerprint}'.format(fingerprint=fingerprint, client_id=client_id), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_15(cls, ):
#    response, _ = cls._call('/gists', method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_16(cls, ):
#    """"Note: With pagination, you can fetch up to 3000 gists. For example, you can fetch 100 pages with 30 gists per page or 30 pages with 100 gists per page."""
#    response, _ = cls._call('/gists/public', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_17(cls, ):
#    """"List the authenticated user's starred gists."""
#    response, _ = cls._call('/gists/starred', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_18(cls, gist_id: int):
#    response, _ = cls._call('/gists/{gist_id}/comments'.format(gist_id=gist_id), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_21(cls, id: int):
#    response, _ = cls._call('/gists/{id}/commits'.format(id=id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_22(cls, id: int):
#    response, _ = cls._call('/gists/{id}/forks'.format(id=id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_25(cls, ):
#    """"List all templates available to pass as an option when creating a repository."""
#    response, _ = cls._call('/gitignore/templates', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_26(cls, ):
#    """"The API also allows fetching the source of a single template."""
#    response, _ = cls._call('/gitignore/templates/c', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_27(cls, ):
#    """"List repositories that are accessible to the authenticated installation."""
#    response, _ = cls._call('/installation/repositories', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_28(cls, installation_id: int):
#    response, _ = cls._call('/installations/{installation_id}/access_tokens'.format(installation_id=installation_id), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_29(cls, ):
#    """"List all issues assigned to the authenticated user across all visible repositories including owned repositories, member repositories, and organization repositories."""
#    response, _ = cls._call('/issues', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_30(cls, ):
#    response, _ = cls._call('/licenses', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_34(cls, ):
#    """"Note: Pagination is powered exclusively by the since parameter. Use the Link header to get the URL for the next page of organizations."""
#    response, _ = cls._call('/organizations', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_36(cls, org: str):
#    """"List the users blocked by an organization."""
#    response, _ = cls._call('/orgs/{org}/blocks'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_37(cls, org: str, username: str):
#    response, _ = cls._call('/orgs/{org}/blocks/{username}'.format(org=org, username=username), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_38(cls, org: str):
#    response, _ = cls._call('/orgs/{org}/hooks'.format(org=org), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_41(cls, org: str):
#    """"The return hash contains a role field which refers to the Organization Invitation role and will be one of the following values: direct_member, admin, billing_manager,  hiring_manager, or reinstate. If the invitee is not a GitHub member, the login field in the return hash will be null."""
#    response, _ = cls._call('/orgs/{org}/invitations'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_42(cls, org: str):
#    """"List all issues for a given organization assigned to the authenticated user."""
#    response, _ = cls._call('/orgs/{org}/issues'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_43(cls, org: str):
#    """"List all users who are members of an organization. If the authenticated user is also a member of this organization then both concealed and public members will be returned."""
#    response, _ = cls._call('/orgs/{org}/members'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_44(cls, org: str, username: str):
#    """"Removing a user from this list will remove them from all teams and they will no longer have any access to the organization's repositories."""
#    response, _ = cls._call('/orgs/{org}/members/{username}'.format(org=org, username=username), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_46(cls, org: str):
#    """"Lists the most recent migrations."""
#    response, _ = cls._call('/orgs/{org}/migrations'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_50(cls, org: str):
#    """"List all users who are outside collaborators of an organization."""
#    response, _ = cls._call('/orgs/{org}/outside_collaborators'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_51(cls, org: str, username: str):
#    """"When an organization member is converted to an outside collaborator, they'll only have access to the repositories that their current team membership allows. The user will no longer be a member of the organization. For more information, see "Converting an organization member to an outside collaborator"."""
#    response, _ = cls._call('/orgs/{org}/outside_collaborators/{username}'.format(org=org, username=username), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_52(cls, org: str):
#    response, _ = cls._call('/orgs/{org}/projects'.format(org=org), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_53(cls, org: str):
#    """"Members of an organization can choose to have their membership publicized or not."""
#    response, _ = cls._call('/orgs/{org}/public_members'.format(org=org), method='GET')
#    return cls.from_response(response)
#
#
#@classmethod
#def func_60(cls, column_id: int):
#    response, _ = cls._call('/projects/columns/{column_id}/cards'.format(column_id=column_id), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_63(cls, project_id: int):
#    response, _ = cls._call('/projects/{project_id}/columns'.format(project_id=project_id), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_68(cls, owner: str, name: str):
#    response, _ = cls._call('/repos/{owner}/{name}/community/profile'.format(owner=owner, name=name), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_70(cls, owner: str, repo: str):
#    """"Lists the available assignees for issues in a repository."""
#    response, _ = cls._call('/repos/{owner}/{repo}/assignees'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_72(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/branches'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_82(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/collaborators'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_84(cls, owner: str, username: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/collaborators/{username}/permission'.format(owner=owner, username=username, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_85(cls, owner: str, repo: str):
#    """"Comments are ordered by ascending ID."""
#    response, _ = cls._call('/repos/{owner}/{repo}/comments'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_87(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/comments/{id}/reactions'.format(owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_88(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/commits'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_89(cls, ref: str, owner: str, repo: str):
#    """"Users with read access can get the SHA-1 of a commit reference."""
#    response, _ = cls._call('/repos/{owner}/{repo}/commits/{ref}'.format(ref=ref, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_90(cls, ref: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/commits/{ref}/comments'.format(ref=ref, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_91(cls, ref: str, owner: str, repo: str):
#    """"Users with pull access can access a combined view of commit statuses for a given ref."""
#    response, _ = cls._call('/repos/{owner}/{repo}/commits/{ref}/status'.format(ref=ref, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_92(cls, ref: str, owner: str, repo: str):
#    """"Users with pull access can view commit statuses for a given ref."""
#    response, _ = cls._call('/repos/{owner}/{repo}/commits/{ref}/statuses'.format(ref=ref, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_93(cls, sha: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/commits/{sha}'.format(sha=sha, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_94(cls, sha: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/commits/{sha}/comments'.format(sha=sha, owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_96(cls, branchname: str, owner: str, repo: str):
#    """"Both :base and :head must be branch names in :repo. To compare branches across other repositories in the same network as :repo, use the format <USERNAME>:branch. For example."""
#    response, _ = cls._call('/repos/{owner}/{repo}/compare/hubot{branchname}...octocat{branchname}'.format(branchname=branchname, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_97(cls, head: str, owner: str, base: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/compare/{base}...{head}'.format(head=head, owner=owner, base=base, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_99(cls, owner: str, repo: str):
#    """"Lists contributors to the specified repository and sorts them by the number of commits per contributor in descending order. This endpoint may return information that is a few hours old because the GitHub REST API v3 caches contributor data to improve performance."""
#    response, _ = cls._call('/repos/{owner}/{repo}/contributors'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_100(cls, owner: str, repo: str):
#    """"Users with repo or repo_deployment scopes can create a deployment for a given ref."""
#    response, _ = cls._call('/repos/{owner}/{repo}/deployments'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_101(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/deployments/{id}'.format(owner=owner, id=id, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_102(cls, owner: str, id: int, repo: str):
#    """"Users with push access can create deployment statuses for a given deployment."""
#    response, _ = cls._call('/repos/{owner}/{repo}/deployments/{id}/statuses'.format(owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_103(cls, owner: str, status_id: int, id: int, repo: str):
#    """"Users with pull access can view a deployment status for a deployment."""
#    response, _ = cls._call('/repos/{owner}/{repo}/deployments/{id}/statuses/{status_id}'.format(owner=owner, status_id=status_id, id=id, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_104(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/downloads'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_105(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/downloads/{id}'.format(owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_107(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/blobs'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_108(cls, sha: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/blobs/{sha}'.format(sha=sha, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_109(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/commits'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_111(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/refs'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_112(cls, owner: str, repo: str):
#    """"If the ref doesn't exist in the repository, but existing refs start with ref they will be returned as an array. For example, a call to get the data for a branch named feature, which doesn't exist, would return head refs including featureA and featureB which do."""
#    response, _ = cls._call('/repos/{owner}/{repo}/git/refs/heads/feature'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_114(cls, owner: str, repo: str):
#    """"The ref in the URL must be formatted as heads/branch, not just branch. For example, the call to get the data for a branch named skunkworkz/featureA would be."""
#    response, _ = cls._call('/repos/{owner}/{repo}/git/refs/heads/skunkworkz/featurea'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_115(cls, owner: str, repo: str):
#    """"You can also request a sub-namespace. For example, to get all the tag references, you can call."""
#    response, _ = cls._call('/repos/{owner}/{repo}/git/refs/tags'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_116(cls, ref: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/refs/{ref}'.format(ref=ref, owner=owner, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_117(cls, owner: str, repo: str):
#    """"Note that creating a tag object does not create the reference that makes a tag in Git.  If you want to create an annotated tag in Git, you have to do this call to create the tag object, and then create the refs/tags/[tag] reference. If you want to create a lightweight tag, you only have to create the tag reference - this call would be unnecessary."""
#    response, _ = cls._call('/repos/{owner}/{repo}/git/tags'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_118(cls, sha: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/tags/{sha}'.format(sha=sha, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_119(cls, owner: str, repo: str):
#    """"The tree creation API will take nested entries as well. If both a tree and a nested path modifying that tree are specified, it will overwrite the contents of that tree with the new path contents and write a new tree out."""
#    response, _ = cls._call('/repos/{owner}/{repo}/git/trees'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_121(cls, sha: str, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/git/trees/{sha}?recursive=1'.format(sha=sha, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_122(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/hooks'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_123(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/hooks/{id}'.format(owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_124(cls, owner: str, id: int, repo: str):
#    """"This will trigger a ping event to be sent to the hook."""
#    response, _ = cls._call('/repos/{owner}/{repo}/hooks/{id}/pings'.format(owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_125(cls, owner: str, id: int, repo: str):
#    """"This will trigger the hook with the latest push to the current repository if the hook is subscribed to push events. If the hook is not subscribed to push events, the server will respond with 204 but no test POST will be generated."""
#    response, _ = cls._call('/repos/{owner}/{repo}/hooks/{id}/tests'.format(owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_127(cls, owner: str, repo: str):
#    """"This API method and the "Map a commit author" method allow you to provide correct Git author information."""
#    response, _ = cls._call('/repos/{owner}/{repo}/import/authors'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_128(cls, owner: str, author_id: int, repo: str):
#    """"Update an author's identity for the import. Your application can continue updating authors any time before you push new commits to the repository."""
#    response, _ = cls._call('/repos/{owner}/{repo}/import/authors/{author_id}'.format(owner=owner, author_id=author_id, repo=repo), method='PATCH')
#    return cls.from_response(response)
#
#@classmethod
#def func_129(cls, owner: str, repo: str):
#    """"List files larger than 100MB found during the impor."""
#    response, _ = cls._call('/repos/{owner}/{repo}/import/large_files'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_130(cls, owner: str, repo: str):
#    """"You can import repositories from Subversion, Mercurial, and TFS that include files larger than 100MB. This ability is powered by Git LFS. You can learn more about our LFS feature and working with large files on our help site."""
#    response, _ = cls._call('/repos/{owner}/{repo}/import/lfs'.format(owner=owner, repo=repo), method='PATCH')
#    return cls.from_response(response)
#
#@classmethod
#def func_131(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/invitations'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_132(cls, owner: str, invitation_id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/invitations/{invitation_id}'.format(owner=owner, invitation_id=invitation_id, repo=repo), method='PATCH')
#    return cls.from_response(response)
#
#@classmethod
#def func_134(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/comments'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_135(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/comments/{id}'.format(owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_136(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/comments/{id}/reactions'.format(owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_137(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/events'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_138(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/events/{id}'.format(owner=owner, id=id, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_141(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/comments'.format(number=number, owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_142(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/events'.format(number=number, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_143(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/labels'.format(number=number, owner=owner, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_146(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/reactions'.format(number=number, owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_147(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/issues/{number}/timeline'.format(number=number, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_148(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/keys'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_149(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/keys/{id}'.format(owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_150(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/labels'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_151(cls, owner: str, name: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/labels/{name}'.format(owner=owner, name=name, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_152(cls, owner: str, repo: str):
#    """"Lists languages for the specified repository. The value shown for each language is the number of bytes of code written in that language."""
#    response, _ = cls._call('/repos/{owner}/{repo}/languages'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_154(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/merges'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_155(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/milestones'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#classmethod
#def func_157(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/milestones/{number}/labels'.format(number=number, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_158(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pages'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_159(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pages/builds'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_160(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pages/builds/latest'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_161(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pages/builds/{id}'.format(owner=owner, id=id, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_162(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/projects'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_163(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_164(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/comments'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_166(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/comments/{id}/reactions'.format(owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_167(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}'.format(number=number, owner=owner, repo=repo), method='PATCH')
#    return cls.from_response(response)
#
#@classmethod
#def func_168(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/comments'.format(number=number, owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_169(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/commits'.format(number=number, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_170(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/files'.format(number=number, owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_171(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/merge'.format(number=number, owner=owner, repo=repo), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_172(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/requested_reviewers'.format(number=number, owner=owner, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_173(cls, number: int, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/reviews'.format(number=number, owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_174(cls, number: int, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/reviews/{id}'.format(number=number, owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_175(cls, number: int, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/reviews/{id}/comments'.format(number=number, owner=owner, id=id, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_176(cls, number: int, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/reviews/{id}/dismissals'.format(number=number, owner=owner, id=id, repo=repo), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_177(cls, number: int, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/pulls/{number}/reviews/{id}/events'.format(number=number, owner=owner, id=id, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_179(cls, owner: str, repo: str):
#    """"Users with push access to the repository can create a release."""
#    response, _ = cls._call('/repos/{owner}/{repo}/releases'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_180(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/releases/assets/{id}'.format(owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_181(cls, owner: str, repo: str):
#    """"View the latest published full release for the repository. Draft releases and prereleases are not returned by this endpoint."""
#    response, _ = cls._call('/repos/{owner}/{repo}/releases/latest'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_184(cls, owner: str, id: int, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/releases/{id}/assets'.format(owner=owner, id=id, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_185(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/stats/code_frequency'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_186(cls, owner: str, repo: str):
#    """"Returns the last year of commit activity grouped by week.  The days array is a group of commits per day, starting on Sunday."""
#    response, _ = cls._call('/repos/{owner}/{repo}/stats/commit_activity'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_187(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/stats/contributors'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_188(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/stats/participation'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_189(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/stats/punch_card'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_190(cls, sha: str, owner: str, repo: str):
#    """"Users with push access can create commit statuses for a given ref."""
#    response, _ = cls._call('/repos/{owner}/{repo}/statuses/{sha}'.format(sha=sha, owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_191(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/tags'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_192(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/teams'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_193(cls, owner: str, repo: str):
#    response, _ = cls._call('/repos/{owner}/{repo}/topics'.format(owner=owner, repo=repo), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_194(cls, owner: str, repo: str):
#    """"Get the total number of clones and breakdown per day or week for the last 14 days. Timestamps are aligned to UTC midnight of the beginning of the day or week. Week begins on Monday."""
#    response, _ = cls._call('/repos/{owner}/{repo}/traffic/clones'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_195(cls, owner: str, repo: str):
#    """"Get the top 10 popular contents over the last 14 days."""
#    response, _ = cls._call('/repos/{owner}/{repo}/traffic/popular/paths'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_196(cls, owner: str, repo: str):
#    """"Get the top 10 referrers over the last 14 days."""
#    response, _ = cls._call('/repos/{owner}/{repo}/traffic/popular/referrers'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_197(cls, owner: str, repo: str):
#    """"Get the total number of views and breakdown per day or week for the last 14 days. Timestamps are aligned to UTC midnight of the beginning of the day or week. Week begins on Monday."""
#    response, _ = cls._call('/repos/{owner}/{repo}/traffic/views'.format(owner=owner, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_198(cls, owner: str, repo: str):
#    """"A transfer request will need to be accepted by the new owner when transferring a personal repository to another user. The response will contain the original owner, and the transfer will continue asynchronously. For more details on the requirements to transfer personal and organization-owned repositories, see about repository transfers."""
#    response, _ = cls._call('/repos/{owner}/{repo}/transfer'.format(owner=owner, repo=repo), method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_199(cls, ref: str, owner: str, archive_format: str, repo: str):
#    """"Note: For private repositories, these links are temporary and expire after five minutes."""
#    response, _ = cls._call('/repos/{owner}/{repo}/{archive_format}/{ref}'.format(ref=ref, owner=owner, archive_format=archive_format, repo=repo), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_200(cls, ):
#    """"Note: Pagination is powered exclusively by the since parameter. Use the Link header to get the URL for the next page of repositories."""
#    response, _ = cls._call('/repositories', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_201(cls, ):
#    """"Find file contents via various criteria. (This method returns up to 100 results per page.."""
#    response, _ = cls._call('/search/code', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_202(cls, ):
#    """"Find commits via various criteria. (This method returns up to 100 results per page.."""
#    response, _ = cls._call('/search/commits', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_203(cls, ):
#    """"Find issues by state and keyword. (This method returns up to 100 results per page.."""
#    response, _ = cls._call('/search/issues', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_204(cls, ):
#    """"Find repositories via various criteria. This method returns up to 100 results per page."""
#    response, _ = cls._call('/search/repositories', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_205(cls, ):
#    """"Find users via various criteria. (This method returns up to 100 results per page.."""
#    response, _ = cls._call('/search/users', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_207(cls, id: int):
#    """"The return hash contains a role field which refers to the Organization Invitation role and will be one of the following values: direct_member, admin, billing_manager, hiring_manager, or reinstate. If the invitee is not a GitHub member, the login field in the return hash will be null."""
#    response, _ = cls._call('/teams/{id}/invitations'.format(id=id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_208(cls, id: int):
#    """"To list members in a team, the team must be visible to the authenticated user."""
#    response, _ = cls._call('/teams/{id}/members'.format(id=id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_209(cls, id: int, username: str):
#    """"To remove a membership between a user and a team, the authenticated user must have 'admin' permissions to the team or be an owner of the organization that the team is associated with. NOTE: This does not delete the user, it just removes their membership from the team."""
#    response, _ = cls._call('/teams/{id}/memberships/{username}'.format(id=id, username=username), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_210(cls, id: int):
#    """"Note: If you pass the hellcat-preview media type, the response will include any repositories inherited through a parent team."""
#    response, _ = cls._call('/teams/{id}/repos'.format(id=id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_211(cls, org: str, id: int, repo: str):
#    """"To add a repository to a team or update the team's permission on a repository, the authenticated user must have admin access to the repository, and must be able to see the team. Also, the repository must be owned by the organization, or a direct fork of a repository owned by the organization."""
#    response, _ = cls._call('/teams/{id}/repos/{org}/{repo}'.format(org=org, id=id, repo=repo), method='PUT')
#    return cls.from_response(response)
#
#@classmethod
#def func_212(cls, owner: str, id: int, repo: str):
#    """"If the authenticated user is an organization owner or a team maintainer, they can remove any repositories from the team. To remove a repository from a team as an organization member, the authenticated user must have admin access to the repository and must be able to see the team. NOTE: This does not delete the repository, it just removes it from the team."""
#    response, _ = cls._call('/teams/{id}/repos/{owner}/{repo}'.format(owner=owner, id=id, repo=repo), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_213(cls, id: int):
#    """"At this time, the hellcat-preview media type is required to use this endpoint."""
#    response, _ = cls._call('/teams/{id}/teams'.format(id=id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_215(cls, ):
#    """"List the users you've blocked on your personal account."""
#    response, _ = cls._call('/user/blocks', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_217(cls, ):
#    response, _ = cls._call('/user/email/visibility', method='PATCH')
#    return cls.from_response(response)
#
#@classmethod
#def func_219(cls, ):
#    """"List the authenticated user's followers."""
#    response, _ = cls._call('/user/followers', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_220(cls, ):
#    """"List who the authenticated user is following."""
#    response, _ = cls._call('/user/following', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_221(cls, username: str):
#    response, _ = cls._call('/user/following/{username}'.format(username=username), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_222(cls, ):
#    """"Creates a GPG key. Requires that you are authenticated via Basic Auth, or OAuth with at least write:gpg_key scope."""
#    response, _ = cls._call('/user/gpg_keys', method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_223(cls, id: int):
#    """"Removes a GPG key. Requires that you are authenticated via Basic Auth or via OAuth with at least admin:gpg_key scope."""
#    response, _ = cls._call('/user/gpg_keys/{id}'.format(id=id), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_224(cls, installation_id: int):
#    """"List repositories that are accessible to the authenticated user for an installation."""
#    response, _ = cls._call('/user/installations/{installation_id}/repositories'.format(installation_id=installation_id), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_225(cls, installation_id: int, repository_id: int):
#    """"Remove a single repository from an installation."""
#    response, _ = cls._call('/user/installations/{installation_id}/repositories/{repository_id}'.format(installation_id=installation_id, repository_id=repository_id), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_227(cls, ):
#    """"List all issues across owned and member repositories assigned to the authenticated user."""
#    response, _ = cls._call('/user/issues', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_228(cls, ):
#    """"Creates a public key. Requires that you are authenticated via Basic Auth, or OAuth with at least write:public_key scope."""
#    response, _ = cls._call('/user/keys', method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_229(cls, id: int):
#    """"Removes a public key. Requires that you are authenticated via Basic Auth or via OAuth with at least admin:public_key scope."""
#    response, _ = cls._call('/user/keys/{id}'.format(id=id), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_230(cls, ):
#    response, _ = cls._call('/user/memberships/orgs', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_231(cls, org: str):
#    response, _ = cls._call('/user/memberships/orgs/{org}'.format(org=org), method='PATCH')
#    return cls.from_response(response)
#
#@classmethod
#def func_233(cls, ):
#    """"Create a new repository for the authenticated user."""
#    response, _ = cls._call('/user/repos', method='POST')
#    return cls.from_response(response)
#
#@classmethod
#def func_234(cls, ):
#    response, _ = cls._call('/user/repository_invitations', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_235(cls, invitation_id: int):
#    response, _ = cls._call('/user/repository_invitations/{invitation_id}'.format(invitation_id=invitation_id), method='DELETE')
#    return cls.from_response(response)
#
#@classmethod
#def func_236(cls, ):
#    """"List all of the teams across all of the organizations to which the authenticated user belongs. This method requires user, repo, or read:org scope when authenticating via OAuth."""
#    response, _ = cls._call('/user/teams', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_237(cls, ):
#    """"Note: Pagination is powered exclusively by the since parameter. Use the Link header to get the URL for the next page of users."""
#    response, _ = cls._call('/users', method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_238(cls, username: str):
#    response, _ = cls._call('/users/{username}'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_239(cls, username: str):
#    """"List a user's followers."""
#    response, _ = cls._call('/users/{username}/followers'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_240(cls, username: str):
#    """"List who a user is following."""
#    response, _ = cls._call('/users/{username}/following'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_241(cls, target_user: str, username: str):
#    response, _ = cls._call('/users/{username}/following/{target_user}'.format(target_user=target_user, username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_242(cls, username: str):
#    """"List public gists for the specified user."""
#    response, _ = cls._call('/users/{username}/gists'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_243(cls, username: str):
#    response, _ = cls._call('/users/{username}/gpg_keys'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_244(cls, username: str):
#    response, _ = cls._call('/users/{username}/keys'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_245(cls, username: str):
#    """"This method only lists public memberships, regardless of authentication. If you need to fetch all of the organization memberships (public and private) for the authenticated user, use the List your organizations API instead."""
#    response, _ = cls._call('/users/{username}/orgs'.format(username=username), method='GET')
#    return cls.from_response(response)
#
#@classmethod
#def func_246(cls, username: str):
#    """"List public repositories for the specified user."""
#    response, _ = cls._call('/users/{username}/repos'.format(username=username), method='GET')
#    return cls.from_response(response)

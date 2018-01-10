"""Schemas of GitHub v3 API response objects."""

from voluptuous import All
from voluptuous import Any
from voluptuous import Optional
from voluptuous import Range
from voluptuous import Required
from voluptuous import Self
from voluptuous import Schema
from voluptuous import Url

import githubcap.enums as enums


USER_SCHEMA = Schema({
    Optional("bio"): str,
    Optional("blog"): str,
    Optional("company"): str,
    Optional("created_at"): str,
    Optional("email"): str,
    Optional("followers"): int,
    Optional("following"): int,
    Optional("hireable"): bool,
    Optional("location"): str,
    Optional("name"): str,
    Optional("public_gists"): int,
    Optional("public_repos"): int,
    Optional("updated_at"): str,
    Required("avatar_url"): Url(),
    Required("events_url"): Url(),
    Required("followers_url"): Url(),
    Required("following_url"): Url(),
    Required("gists_url"): Url(),
    Required("gravatar_id"): str,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("login"): str,
    Required("organizations_url"): Url(),
    Required("received_events_url"): Url(),
    Required("repos_url"): Url(),
    Required("site_admin"): bool,
    Required("starred_url"): Url(),
    Required("subscriptions_url"): Url(),
    Required("type"): Schema(Any(*enums.UserType.all_values())),
    Required("url"): Url(),
})


REPOSITORY_PERMISSIONS_SCHEMA = Schema({
    Required("admin"): bool,
    Required("pull"): bool,
    Required("push"): bool
})


ORGANIZATION_SCHEMA = Schema({
    Required("avatar_url"): Url(),
    Required("description"): str,
    Required("events_url"): Url(),
    Required("hooks_url"): Url(),
    Required("id"): int,
    Required("issues_url"): Url(),
    Required("login"): str,
    Required("members_url"): Url(),
    Required("public_members_url"): Url(),
    Required("repos_url"): Url(),
    Required("url"): Url(),
})


LICENSE_SCHEMA = Schema({
    Required("key"): str,
    Required("name"): str,
    Required("spdx_id"): Schema(Any(str, None)),
    Required("url"): Schema(Any(Url(), None))
})


REPOSITORY_SCHEMA = Schema({
    Optional("allow_merge_commit"): bool,
    Optional("allow_rebase_merge"): bool,
    Optional("allow_squash_merge"): bool,
    Optional("network_count"): int,
    Optional("permissions"): REPOSITORY_PERMISSIONS_SCHEMA,
    Optional("subscribers_count"): int,
    Optional("topics"): [str],
    Required("archived"): bool,
    Required("archive_url"): Url(),
    Required("assignees_url"): Url(),
    Required("blobs_url"): Url(),
    Required("branches_url"): Url(),
    Required("clone_url"): Url(),
    Required("collaborators_url"): Url(),
    Required("comments_url"): Url(),
    Required("commits_url"): Url(),
    Required("compare_url"): Url(),
    Required("contents_url"): Url(),
    Required("contributors_url"): Url(),
    Required("created_at"): str,
    Required("default_branch"): str,
    Required("deployments_url"): Url(),
    Required("description"): Schema(Any(str, None)),
    Required("downloads_url"): Url(),
    Required("events_url"): Url(),
    Required("fork"): bool,
    Required("forks_count"): int,
    Required("forks"): int,
    Required("forks_url"): Url(),
    Required("full_name"): str,
    Required("git_commits_url"): Url(),
    Required("git_refs_url"): Url(),
    Required("git_tags_url"): Url(),
    Required("git_url"): Url(),
    Required("has_downloads"): bool,
    Required("has_issues"): bool,
    Required("has_pages"): bool,
    Required("has_projects"): bool,
    Required("has_wiki"): bool,
    Required("homepage"): Schema(Any(str, None)),
    Required("hooks_url"): Url(),
    Required("html_url"): Url(),
    Required("id"): int,
    Required("issue_comment_url"): Url(),
    Required("issue_events_url"): Url(),
    Required("issues_url"): Url(),
    Required("keys_url"): Url(),
    Required("labels_url"): Url(),
    Required("language"): Schema(Any(None, str)),
    Required("languages_url"): Url(),
    Required("license"): Schema(Any(LICENSE_SCHEMA, None)),
    Required("merges_url"): Url(),
    Required("milestones_url"): Url(),
    Required("mirror_url"): Schema(Any(Url(), None)),
    Required("name"): str,
    Required("notifications_url"): Url(),
    Required("open_issues_count"): int,
    Required("open_issues"): int,
    Required("owner"): USER_SCHEMA,
    Required("private"): bool,
    Required("pulls_url"): Url(),
    Required("pushed_at"): str,
    Required("releases_url"): Url(),
    Required("size"): int,
    Required("ssh_url"): str,  # Not recognized by Url()
    Required("stargazers_count"): int,
    Required("stargazers_url"): Url(),
    Required("statuses_url"): Url(),
    Required("subscribers_url"): Url(),
    Required("subscription_url"): Url(),
    Required("svn_url"): Url(),
    Required("tags_url"): Url(),
    Required("teams_url"): Url(),
    Required("trees_url"): Url(),
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("watchers_count"): int,
    Required("watchers"): int,
})


APP_SCHEMA = Schema({
    Required("client_id"): str,
    Required("name"): str,
    Required("url"): Url()
})


AUTHORIZATION_SCHEMA = Schema({
    Required("app"): APP_SCHEMA,
    Required("created_at"): str,
    Required("fingerprint"): str,
    Required("hashed_token"): str,
    Required("id"): int,
    Required("note"): str,
    Required("note_url"): Url(),
    Required("scopes"):  Schema(Any(*enums.AuthorizationScope.all_values())),
    Required("token_last_eight"): str,
    Required("token"): str,
    Required("updated_at"): str,
    Required("url"): Url(),
})


AUTHORIZATION_INFO_SCHEMA = Schema({
    Required("app"): APP_SCHEMA,
    Required("created_at"): str,
    Required("fingerprint"): str,
    Required("hashed_token"): str,
    Required("id"): int,
    Required("note"): str,
    Required("note_url"): Url(),
    Required("scopes"):  Schema(Any(*enums.AuthorizationScope.all_values())),
    Required("token_last_eight"): str,
    Required("token"): str,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


THREAD_SUBSCRIPTION_SCHEMA = Schema({
    Required("created_at"): str,
    Required("ignored"): bool,
    Required("reason"): Schema(Any(None, str)),
    Required("subscribed"): bool,
    Required("thread_url"): Url(),
    Required("url"): Url(),
})


GIST_FORK_SCHEMA = Schema({
    Required("created_at"): str,
    Required("id"): str,
    Required("updated_at"): str,
    Required("url"): str,
    Required("user"): USER_SCHEMA,
})


GIST_HISTORY_SCHEMA = Schema({
    Required("committed_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
    Required("version"): str,
    Required("change_status"): Schema({
        Required('deletions'): int,
        Required('additions'): int,
        Required('total'): int
    }),
})


GIST_SCHEMA = Schema({
    Required("comments"): int,
    Required("comments_url"): Url(),
    Required("commits_url"): Url(),
    Required("created_at"): str,
    Required("description"): str,
    Required("files"): dict,
    Required("forks"): [GIST_FORK_SCHEMA],
    Required("forks_url"): Url(),
    Required("git_pull_url"): Url(),
    Required("git_push_url"): Url(),
    Required("history"): [GIST_HISTORY_SCHEMA],
    Required("html_url"): Url(),
    Required("id"): str,
    Required("owner"): dict,
    Required("public"): bool,
    Required("truncated"): bool,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


GIST_COMMENT_SCHEMA = Schema({
    Required("body"): str,
    Required("created_at"): str,
    Required("id"): int,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


COMMIT_REF_SCHEMA = Schema({
    Required("sha"): str,
    Required("url"): Url(),
})


COMMIT_PERSON_INFO = Schema({
    Required("date"): str,
    Required("email"): str,
    Required("name"): str,
})


COMMIT_SCHEMA = Schema({
    Required("author"): COMMIT_PERSON_INFO,
    Required("committer"): COMMIT_PERSON_INFO,
    Required("message"): str,
    Required("parents"): [COMMIT_REF_SCHEMA],
    Required("sha"): str,
    Required("tree"): COMMIT_REF_SCHEMA,
    Required("url"): Url(),
    Required("verification"): dict,
})


GIT_OBJECT_SCHEMA = Schema({
    Required("sha"): str,
    Required("type"): str,
    Required("url"): str,
})


SCHEMA = Schema({
    Required("ref"): str,
    Required("url"): Url(),
    Required("object"): GIT_OBJECT_SCHEMA,
})


GIT_VERIFICATION_SCHEMA = Schema({
    Required("payload"): object,
    Required("reason"): str,
    Required("signature"): object,
    Required("verified"): bool,
})


GIT_TAG_SCHEMA = Schema({
    Required("message"): str,
    Required("object"): GIT_OBJECT_SCHEMA,
    Required("sha"): str,
    Required("tagger"): USER_SCHEMA,
    Required("tag"): str,
    Required("url"): Url(),
    Required("verification"): GIT_VERIFICATION_SCHEMA,
})


GIT_TREE_STRUCTURE_SCHEMA = Schema({
    Optional("size"): int,
    Optional("url"): str,
    Required("mode"): int,
    Required("path"): str,
    Required("sha"): str,
    Required("type"): Schema(Any(*enums.GitTreeType.all_values())),
    Required("type"): str,
})


GIT_TREE_SCHEMA = Schema({
    Required("sha"): str,
    Required("tree"): [GIT_TREE_STRUCTURE_SCHEMA],
    Required("truncated"): bool,
    Required("url"): Url(),
})


GITHUB_APP_SCHEMA = Schema({
    Required("created_at"): str,
    Required("description"): str,
    Required("external_url"): Url(),
    Required("html_url"): Url(),
    Required("id"): int,
    Required("name"): str,
    Required("owner"): USER_SCHEMA,
    Required("updated_at"): str,
})
 

REPOSITORIES_LISTING_SCHEMA = Schema({
    Required("repositories"): [REPOSITORY_SCHEMA],
    Required("total_count"): int,
})


ISSUE_COMMENT_SCHEMA = Schema({
    Required("body"): str,
    Required("created_at"): str,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


LABEL_SCHEMA = Schema({
    Required("color"): str,
    Required("default"): bool,
    Required("id"): int,
    Required("name"): str,
    Required("url"): Url(),
})


MILESTONE_SCHEMA = Schema({
    Required("closed_at"): Schema(Any(str, None)),
    Required("closed_issues"): int,
    Required("created_at"): str,
    Required("creator"): USER_SCHEMA,
    Required("description"): Schema(Any(str, None)),
    Required("due_on"): Schema(Any(str, None)),
    Required("html_url"): Url(),
    Required("id"): int,
    Required("labels_url"): Url(),
    Required("number"): int,
    Required("open_issues"): int,
    Required("state"): str,
    Required("title"): str,
    Required("updated_at"): Schema(Any(str, None)),
    Required("url"): Url(),
})


MIGRATION_SCHEMA = Schema({
    Required("created_at"): str,
    Required("exclude_attachments"): bool,
    Required("guid"): str,
    Required("id"): int,
    Required("lock_repositories"): bool,
    Required("repositories"): [REPOSITORY_SCHEMA],
    Required("state"): str,
    Required("updated_at"): str,
    Required("url"): Url(),
})


SOURCE_IMPORT_SCHEMA = Schema({
    Required("authors_count"): int,
    Required("authors_url"): Url(),
    Required("commit_count"): int,
    Required("has_large_files"): bool,
    Required("html_url"): Url(),
    Required("large_files_count"): int,
    Required("large_files_size"): int,
    Required("percent"): int,
    Required("repository_url"): Url(),
    Required("status"): str,
    Required("status_text"): str,
    Required("url"): Url(),
    Required("use_lfs"): str,
    Required("vcs"): str,
    Required("vcs_url"): Url(),
})


CODE_OF_CONDUCT_SCHEMA = Schema({
    Required("body"): str,
    Required("key"): str,
    Required("name"): str,
    Required("url"): Url(),
})


ORGANIZATION_MEMBERSHIP_SCHEMA = Schema({
    Required("organization"): ORGANIZATION_SCHEMA,
    Required("organization_url"): Url(),
    Required("role"):  Schema(Any(*enums.OrganizationRole.all_values())),
    Required("state"):  Schema(Any(*enums.OrganizationState.all_values())),
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


ERROR_REPORT_SCHEMA = Schema({
    Optional("documentation_url"): Url(),
    Required("message"): str,
})


ERROR_TEAM_SCHEMA = Schema({
    Required("errors"): [list],
    Required("message"): str,
})


HOOK_SCHEMA = Schema({
    Optional("test_url"): Url(),
    Required("active"): bool,
    Required("config"): dict,
    Required("created_at"): str,
    Required("events"):  [Schema(Any(*enums.OrganizationState.all_values()))],
    Required("id"): int,
    Required("name"): str,
    Required("ping_url"): Url(),
    Required("updated_at"): str,
    Required("url"): Url(),
})


PROJECT_CARD_SCHEMA = Schema({
    Required("column_url"): Url(),
    Required("content_url"): Url(),
    Required("created_at"): str,
    Required("creator"): USER_SCHEMA,
    Required("id"): int,
    Required("note"): str,
    Required("updated_at"): str,
    Required("url"): Url(),
})


PROJECT_COLUMN_SCHEMA = Schema({
    Required("cards_url"): Url(),
    Required("created_at"): str,
    Required("id"): int,
    Required("name"): str,
    Required("project_url"): Url(),
    Required("updated_at"): str,
    Required("url"): Url(),
})


BRANCH_SCHEMA = Schema({
    Required("label"): str,
    Required("ref"): str,
    Required("repo"): REPOSITORY_SCHEMA,
    Required("sha"): str,
    Required("user"): USER_SCHEMA,
})


PULL_REQUEST_SCHEMA = Schema({
    Required("assignee"): USER_SCHEMA,
    Required("base"): BRANCH_SCHEMA,
    Required("body"): str,
    Required("closed_at"): str,
    Required("comments_url"): Url(),
    Required("commits_url"): Url(),
    Required("created_at"): str,
    Required("diff_url"): Url(),
    Required("head"): BRANCH_SCHEMA,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("issue_url"): Url(),
    Required("_links"): dict,
    Required("locked"): bool,
    Required("merged_at"): str,
    Required("milestone"): MILESTONE_SCHEMA,
    Required("number"): int,
    Required("patch_url"): Url(),
    Required("review_comments_url"): Url(),
    Required("review_comment_url"): Url(),
    Required("state"): str,
    Required("statuses_url"): Url(),
    Required("title"): str,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


REVIEW_SCHEMA = Schema({
    Required("body"): str,
    Required("commit_id"): str,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("_links"): dict,
    Required("pull_request_url"): Url(),
    Required("state"): Schema(Any(*enums.ReviewState.all_values())),
    Required("user"): USER_SCHEMA,
})


PULL_REQUEST_COMMENT_SCHEMA = Schema({
    Required("body"): str,
    Required("commit_id"): str,
    Required("created_at"): str,
    Required("diff_hunk"): str,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("in_reply_to_id"): int,
    Required("_links"): dict,
    Required("original_commit_id"): str,
    Required("original_position"): int,
    Required("path"): str,
    Required("position"): int,
    Required("pull_request_review_id"): int,
    Required("pull_request_url"): Url(),
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


COMMENT_REACTION_SCHEMA = Schema({
    Required("content"):  Schema(Any(*enums.ReactionType.all_values())),
    Required("content"): str,
    Required("created_at"): str,
    Required("id"): int,
    Required("user"): USER_SCHEMA,
})


TOPICS_LISTING_SCHEMA = Schema({
    Required("names"): [list],
})


COMMIT_COMMENT_SCHEMA = Schema({
    Required("body"): str,
    Required("commit_id"): str,
    Required("created_at"): str,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("line"): int,
    Required("path"): str,
    Required("position"): int,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
})


CONTENT_ENTRY_SCHEMA = Schema({
    Required("download_url"): Url(),
    Required("git_url"): Url(),
    Required("html_url"): Url(),
    Required("_links"): dict,
    Required("name"): str,
    Required("path"): str,
    Required("sha"): str,
    Required("size"): int,
    Required("type"): str,
    Required("url"): Url(),
})


CONTENT_SCHEMA = Schema({
    Required("commit"): COMMIT_SCHEMA,
    Required("content"): Schema(Any(CONTENT_ENTRY_SCHEMA, None)),
})


KEY_SCHEMA = Schema({
    Required("created_at"): str,
    Required("id"): int,
    Required("key"): str,
    Required("read_only"): bool,
    Required("title"): str,
    Required("url"): Url(),
    Required("verified"): bool,
})


INVITATION_SCHEMA = Schema({
    Required("created_at"): str,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("invitee"): USER_SCHEMA,
    Required("inviter"): USER_SCHEMA,
    Required("permissions"): REPOSITORY_PERMISSIONS_SCHEMA,
    Required("repository"): dict,
    Required("url"): Url(),
})


RELEASE_ASSET_SCHEMA = Schema({
    Required("browser_download_url"): Url(),
    Required("content_type"): str,
    Required("created_at"): str,
    Required("download_count"): int,
    Required("id"): int,
    Required("label"): str,
    Required("name"): str,
    Required("size"): int,
    Required("updated_at"): str,
    Required("uploader"): USER_SCHEMA,
    Required("url"): Url(),
})


RELEASE_SCHEMA = Schema({
    Required("assets"): [RELEASE_ASSET_SCHEMA],
    Required("assets_url"): Url(),
    Required("author"): USER_SCHEMA,
    Required("body"): str,
    Required("browser_download_url"): Url(),
    Required("content_type"): str,
    Required("created_at"): str,
    Required("download_count"): int,
    Required("draft"): bool,
    Required("html_url"): Url(),
    Required("id"): int,
    Required("label"): str,
    Required("name"): str,
    Required("prerelease"): bool,
    Required("published_at"): str,
    Required("size"): int,
    Required("state"): Schema(Any(*enums.ReleaseState.all_values())),
    Required("tag_name"): str,
    Required("tarball_url"): Url(),
    Required("target_commitish"): str,
    Required("updated_at"): str,
    Required("uploader"): USER_SCHEMA,
    Required("upload_url"): Url(),
    Required("url"): Url(),
    Required("zipball_url"): Url(),
})


SEARCH_RESULT  =  Schema({
    Required("fragment"): str,
    Required("matches"): [dict],
    Required("object_type"): str,
    Required("object_url"): Url(),
    Required("property"): str,
})


SEARCH_RESULTS_SCHEMA = Schema({
    Required("text_matches"): [SEARCH_RESULT],
})


GPG_KEYS_SCHEMA = Schema({
    Required("id"): int,
    Required("primary_key_id"): Schema(Any(str, None)),
    Required("key_id"): str,
    Required("public_key"): str,
    Required("emails"): [Schema({
        Required("email"): str,
        Required("verified"): True,
    })],
    Required("subkeys"): [Self],
    Required("can_sign"): bool,
    Required("can_encrypt_comms"): bool,
    Required("can_encrypt_storage"): bool,
    Required("can_certify"): bool,
    Required("created_at"): str,
    Required("expires_at"): Schema(Any(str, None)),
})


ISSUE_SCHEMA = Schema({
    Optional("assignee"): object,
    Optional("closed_by"): Schema(Any(USER_SCHEMA, None)),
    Optional("repository"): REPOSITORY_SCHEMA,
    Required("assignees"): [USER_SCHEMA],
    Required("author_association"): Schema(Any(*enums.AuthorAssociation.all_values())),
    Required("body"): Schema(Any(str, None)),
    Required("closed_at"): Schema(Any(str, None)),
    Required("comments"): All(Range(min=0)),
    Required("comments_url"): Url(),
    Required("created_at"): str,
    Required("events_url"): Url(),
    Required("html_url"): Url(),
    Required("id"): All(Range(min=1)),
    Required("labels"): [LABEL_SCHEMA],
    Required("labels_url"): Url(),
    Required("locked"): bool,
    Required("milestone"): Schema(Any(MILESTONE_SCHEMA, None)),
    Required("number"): int,
    Required("repository_url"): Url(),
    Required("state"): Schema(Any(*enums.IssueState.all_values())),
    Required("title"): str,
    Required("updated_at"): str,
    Required("url"): Url(),
    Required("user"): USER_SCHEMA,
    Optional("pull_request"): Schema({  # if this is present, it's a pull request, an issue otherwise
        Required("url"): Url(),
        Required("html_url"): Url(),
        Required("diff_url"): Url(),
        Required("patch_url"): Url()
    }),
})

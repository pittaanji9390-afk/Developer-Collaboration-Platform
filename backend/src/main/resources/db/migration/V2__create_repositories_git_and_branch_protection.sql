-- V2: Repositories, Git, Topics, Stars, Forks, and Branch Protection
CREATE TABLE IF NOT EXISTS repositories (
    id VARCHAR(36) PRIMARY KEY,
    owner_user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    visibility VARCHAR(30) NOT NULL DEFAULT 'PUBLIC',
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    default_branch VARCHAR(100) NOT NULL DEFAULT 'main',
    repository_path VARCHAR(500) NOT NULL,
    size_bytes BIGINT NOT NULL DEFAULT 0,
    fork_count INT NOT NULL DEFAULT 0,
    star_count INT NOT NULL DEFAULT 0,
    watch_count INT NOT NULL DEFAULT 0,
    open_issues_count INT NOT NULL DEFAULT 0,
    open_prs_count INT NOT NULL DEFAULT 0,
    parent_repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE SET NULL,
    allow_forking BOOLEAN NOT NULL DEFAULT TRUE,
    allow_merge_commit BOOLEAN NOT NULL DEFAULT TRUE,
    allow_squash_merge BOOLEAN NOT NULL DEFAULT TRUE,
    allow_rebase_merge BOOLEAN NOT NULL DEFAULT TRUE,
    delete_branch_on_merge BOOLEAN NOT NULL DEFAULT FALSE,
    has_issues BOOLEAN NOT NULL DEFAULT TRUE,
    has_projects BOOLEAN NOT NULL DEFAULT TRUE,
    has_discussions BOOLEAN NOT NULL DEFAULT TRUE,
    has_wiki BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archived_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_repos_owner ON repositories(owner_user_id);
CREATE INDEX idx_repos_org ON repositories(organization_id);
CREATE INDEX idx_repos_slug ON repositories(slug);
CREATE INDEX idx_repos_visibility ON repositories(visibility);

CREATE TABLE IF NOT EXISTS repository_collaborators (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    permission VARCHAR(30) NOT NULL DEFAULT 'WRITE',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_repo_collaborator UNIQUE (repository_id, user_id)
);

CREATE TABLE IF NOT EXISTS team_repository_permissions (
    id VARCHAR(36) PRIMARY KEY,
    team_id VARCHAR(36) NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    permission VARCHAR(30) NOT NULL DEFAULT 'WRITE',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_team_repo_perm UNIQUE (team_id, repository_id)
);

CREATE TABLE IF NOT EXISTS repository_topics (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    topic VARCHAR(50) NOT NULL,
    CONSTRAINT uq_repo_topic UNIQUE (repository_id, topic)
);

CREATE INDEX idx_topics_name ON repository_topics(topic);

CREATE TABLE IF NOT EXISTS repository_stars (
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (repository_id, user_id)
);

CREATE TABLE IF NOT EXISTS repository_watchers (
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_level VARCHAR(30) NOT NULL DEFAULT 'ALL_ACTIVITY',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (repository_id, user_id)
);

CREATE TABLE IF NOT EXISTS branch_protection_rules (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    branch_pattern VARCHAR(100) NOT NULL,
    require_pull_request BOOLEAN NOT NULL DEFAULT TRUE,
    required_approving_review_count INT NOT NULL DEFAULT 1,
    dismiss_stale_reviews BOOLEAN NOT NULL DEFAULT FALSE,
    require_code_owner_reviews BOOLEAN NOT NULL DEFAULT FALSE,
    require_status_checks BOOLEAN NOT NULL DEFAULT FALSE,
    required_status_checks_json TEXT,
    require_conversation_resolution BOOLEAN NOT NULL DEFAULT TRUE,
    require_signed_commits BOOLEAN NOT NULL DEFAULT FALSE,
    require_linear_history BOOLEAN NOT NULL DEFAULT FALSE,
    allow_force_pushes BOOLEAN NOT NULL DEFAULT FALSE,
    allow_deletions BOOLEAN NOT NULL DEFAULT FALSE,
    block_creations BOOLEAN NOT NULL DEFAULT FALSE,
    enforce_admins BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_repo_branch_rule UNIQUE (repository_id, branch_pattern)
);

CREATE TABLE IF NOT EXISTS repository_releases (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    tag_name VARCHAR(100) NOT NULL,
    target_commitish VARCHAR(100) NOT NULL DEFAULT 'main',
    name VARCHAR(255) NOT NULL,
    body TEXT,
    draft BOOLEAN NOT NULL DEFAULT FALSE,
    prerelease BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT uq_repo_release_tag UNIQUE (repository_id, tag_name)
);

CREATE TABLE IF NOT EXISTS release_assets (
    id VARCHAR(36) PRIMARY KEY,
    release_id VARCHAR(36) NOT NULL REFERENCES repository_releases(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    content_type VARCHAR(100) NOT NULL,
    size_bytes BIGINT NOT NULL,
    download_count INT NOT NULL DEFAULT 0,
    storage_path VARCHAR(500) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

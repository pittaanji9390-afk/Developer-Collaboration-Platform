from common_writer import write_file

v1_sql = """-- V1: Core Identity, Users, Organizations, Teams, and Permissions
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url VARCHAR(500),
    bio VARCHAR(500),
    company VARCHAR(100),
    location VARCHAR(100),
    website VARCHAR(255),
    social_links_json TEXT,
    role VARCHAR(30) NOT NULL DEFAULT 'USER',
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);

CREATE TABLE IF NOT EXISTS user_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL UNIQUE,
    user_agent VARCHAR(500),
    ip_address VARCHAR(45),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(refresh_token_hash);

CREATE TABLE IF NOT EXISTS user_verifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(30) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_verifications_token ON user_verifications(token);

CREATE TABLE IF NOT EXISTS user_followers (
    follower_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    following_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, following_id)
);

CREATE TABLE IF NOT EXISTS organizations (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(150),
    description VARCHAR(500),
    avatar_url VARCHAR(500),
    website VARCHAR(255),
    location VARCHAR(100),
    visibility VARCHAR(30) NOT NULL DEFAULT 'PUBLIC',
    billing_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_organizations_slug ON organizations(slug);

CREATE TABLE IF NOT EXISTS organization_members (
    id VARCHAR(36) PRIMARY KEY,
    organization_id VARCHAR(36) NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(30) NOT NULL DEFAULT 'MEMBER',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_org_member UNIQUE (organization_id, user_id)
);

CREATE INDEX idx_org_members_org ON organization_members(organization_id);
CREATE INDEX idx_org_members_user ON organization_members(user_id);

CREATE TABLE IF NOT EXISTS organization_invitations (
    id VARCHAR(36) PRIMARY KEY,
    organization_id VARCHAR(36) NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    inviter_id VARCHAR(36) NOT NULL REFERENCES users(id),
    email VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL DEFAULT 'MEMBER',
    token VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS teams (
    id VARCHAR(36) PRIMARY KEY,
    organization_id VARCHAR(36) NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    privacy VARCHAR(30) NOT NULL DEFAULT 'VISIBLE',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_team_org_slug UNIQUE (organization_id, slug)
);

CREATE TABLE IF NOT EXISTS team_members (
    id VARCHAR(36) PRIMARY KEY,
    team_id VARCHAR(36) NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(30) NOT NULL DEFAULT 'MEMBER',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_team_member UNIQUE (team_id, user_id)
);
"""
write_file("backend/src/main/resources/db/migration/V1__create_core_identity_and_organizations.sql", v1_sql)

v2_sql = """-- V2: Repositories, Git, Topics, Stars, Forks, and Branch Protection
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
"""
write_file("backend/src/main/resources/db/migration/V2__create_repositories_git_and_branch_protection.sql", v2_sql)

v3_sql = """-- V3: Issues, Pull Requests, Code Reviews, Inline Comments, Milestones, Labels
CREATE TABLE IF NOT EXISTS milestones (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    state VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    due_date TIMESTAMP WITH TIME ZONE,
    closed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS labels (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(20) NOT NULL DEFAULT '#0284c7',
    description VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS issues (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    priority VARCHAR(30) NOT NULL DEFAULT 'MEDIUM',
    milestone_id VARCHAR(36) REFERENCES milestones(id) ON DELETE SET NULL,
    locked BOOLEAN NOT NULL DEFAULT FALSE,
    comments_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP WITH TIME ZONE,
    closed_by_id VARCHAR(36) REFERENCES users(id),
    CONSTRAINT uq_repo_issue_num UNIQUE (repository_id, number)
);

CREATE INDEX idx_issues_repo ON issues(repository_id);
CREATE INDEX idx_issues_status ON issues(status);
CREATE INDEX idx_issues_author ON issues(author_id);

CREATE TABLE IF NOT EXISTS issue_assignees (
    issue_id VARCHAR(36) NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (issue_id, user_id)
);

CREATE TABLE IF NOT EXISTS issue_label_assignments (
    issue_id VARCHAR(36) NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
    label_id VARCHAR(36) NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (issue_id, label_id)
);

CREATE TABLE IF NOT EXISTS issue_comments (
    id VARCHAR(36) PRIMARY KEY,
    issue_id VARCHAR(36) NOT NULL REFERENCES issues(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    body TEXT NOT NULL,
    edited BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pull_requests (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT,
    source_branch VARCHAR(100) NOT NULL,
    target_branch VARCHAR(100) NOT NULL,
    source_repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE SET NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    draft BOOLEAN NOT NULL DEFAULT FALSE,
    mergeable BOOLEAN NOT NULL DEFAULT TRUE,
    merge_strategy VARCHAR(30),
    merged_at TIMESTAMP WITH TIME ZONE,
    merged_by_id VARCHAR(36) REFERENCES users(id),
    closed_at TIMESTAMP WITH TIME ZONE,
    closed_by_id VARCHAR(36) REFERENCES users(id),
    milestone_id VARCHAR(36) REFERENCES milestones(id) ON DELETE SET NULL,
    base_commit_sha VARCHAR(64),
    head_commit_sha VARCHAR(64),
    merge_commit_sha VARCHAR(64),
    additions_count INT NOT NULL DEFAULT 0,
    deletions_count INT NOT NULL DEFAULT 0,
    changed_files_count INT NOT NULL DEFAULT 0,
    comments_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_repo_pr_num UNIQUE (repository_id, number)
);

CREATE INDEX idx_prs_repo ON pull_requests(repository_id);
CREATE INDEX idx_prs_status ON pull_requests(status);
CREATE INDEX idx_prs_author ON pull_requests(author_id);

CREATE TABLE IF NOT EXISTS pr_assignees (
    pull_request_id VARCHAR(36) NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (pull_request_id, user_id)
);

CREATE TABLE IF NOT EXISTS pr_review_requests (
    pull_request_id VARCHAR(36) NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    reviewer_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (pull_request_id, reviewer_id)
);

CREATE TABLE IF NOT EXISTS pr_label_assignments (
    pull_request_id VARCHAR(36) NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    label_id VARCHAR(36) NOT NULL REFERENCES labels(id) ON DELETE CASCADE,
    PRIMARY KEY (pull_request_id, label_id)
);

CREATE TABLE IF NOT EXISTS pull_request_reviews (
    id VARCHAR(36) PRIMARY KEY,
    pull_request_id VARCHAR(36) NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    commit_sha VARCHAR(64) NOT NULL,
    body TEXT,
    state VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    submitted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_threads (
    id VARCHAR(36) PRIMARY KEY,
    pull_request_id VARCHAR(36) NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    line_number INT NOT NULL,
    side VARCHAR(10) NOT NULL DEFAULT 'RIGHT',
    commit_sha VARCHAR(64) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    resolved_by_id VARCHAR(36) REFERENCES users(id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_comments (
    id VARCHAR(36) PRIMARY KEY,
    thread_id VARCHAR(36) NOT NULL REFERENCES review_threads(id) ON DELETE CASCADE,
    review_id VARCHAR(36) REFERENCES pull_request_reviews(id) ON DELETE SET NULL,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    body TEXT NOT NULL,
    diff_hunk TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pr_status_checks (
    id VARCHAR(36) PRIMARY KEY,
    pull_request_id VARCHAR(36) NOT NULL REFERENCES pull_requests(id) ON DELETE CASCADE,
    context VARCHAR(100) NOT NULL,
    state VARCHAR(30) NOT NULL,
    target_url VARCHAR(500),
    description VARCHAR(255),
    commit_sha VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_pr_status_context UNIQUE (pull_request_id, context, commit_sha)
);

CREATE TABLE IF NOT EXISTS reactions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content_type VARCHAR(30) NOT NULL,
    content_id VARCHAR(36) NOT NULL,
    reaction_type VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_reaction UNIQUE (user_id, content_type, content_id, reaction_type)
);
"""
write_file("backend/src/main/resources/db/migration/V3__create_issues_pull_requests_and_reviews.sql", v3_sql)

v4_sql = """-- V4: Discussions, Categories, Kanban Project Boards, Columns, Cards
CREATE TABLE IF NOT EXISTS discussion_categories (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    emoji VARCHAR(20) NOT NULL DEFAULT '💬',
    description VARCHAR(255),
    is_qa BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS discussions (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    category_id VARCHAR(36) NOT NULL REFERENCES discussion_categories(id),
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    locked BOOLEAN NOT NULL DEFAULT FALSE,
    pinned BOOLEAN NOT NULL DEFAULT FALSE,
    accepted_answer_comment_id VARCHAR(36),
    comments_count INT NOT NULL DEFAULT 0,
    upvotes_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS discussion_comments (
    id VARCHAR(36) PRIMARY KEY,
    discussion_id VARCHAR(36) NOT NULL REFERENCES discussions(id) ON DELETE CASCADE,
    author_id VARCHAR(36) NOT NULL REFERENCES users(id),
    parent_comment_id VARCHAR(36) REFERENCES discussion_comments(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    is_answer BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_boards (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    owner_user_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    state VARCHAR(30) NOT NULL DEFAULT 'OPEN',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_columns (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL REFERENCES project_boards(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    position INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_cards (
    id VARCHAR(36) PRIMARY KEY,
    column_id VARCHAR(36) NOT NULL REFERENCES project_columns(id) ON DELETE CASCADE,
    issue_id VARCHAR(36) REFERENCES issues(id) ON DELETE SET NULL,
    pull_request_id VARCHAR(36) REFERENCES pull_requests(id) ON DELETE SET NULL,
    note TEXT,
    position INT NOT NULL DEFAULT 0,
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""
write_file("backend/src/main/resources/db/migration/V4__create_discussions_and_project_boards.sql", v4_sql)

v5_sql = """-- V5: Webhooks, Webhook Deliveries, CI/CD Workflows, Runs, Jobs, Steps, Runners, and Secrets Vault
CREATE TABLE IF NOT EXISTS webhooks (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    secret VARCHAR(255) NOT NULL,
    content_type VARCHAR(30) NOT NULL DEFAULT 'JSON',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    events_json TEXT NOT NULL,
    insecure_ssl BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS webhook_deliveries (
    id VARCHAR(36) PRIMARY KEY,
    webhook_id VARCHAR(36) NOT NULL REFERENCES webhooks(id) ON DELETE CASCADE,
    event VARCHAR(50) NOT NULL,
    delivery_guid VARCHAR(64) NOT NULL UNIQUE,
    payload_json TEXT NOT NULL,
    request_headers_json TEXT,
    response_headers_json TEXT,
    response_body TEXT,
    status_code INT,
    duration_ms BIGINT,
    status VARCHAR(30) NOT NULL,
    attempts_count INT NOT NULL DEFAULT 1,
    next_retry_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_webhook_deliv_webhook ON webhook_deliveries(webhook_id);
CREATE INDEX idx_webhook_deliv_status ON webhook_deliveries(status);

CREATE TABLE IF NOT EXISTS secrets (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    encrypted_value TEXT NOT NULL,
    iv VARCHAR(64) NOT NULL,
    auth_tag VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_repo_secret UNIQUE (repository_id, name)
);

CREATE TABLE IF NOT EXISTS ci_runners (
    id VARCHAR(36) PRIMARY KEY,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    token VARCHAR(100) NOT NULL UNIQUE,
    os VARCHAR(50) NOT NULL DEFAULT 'LINUX',
    architecture VARCHAR(50) NOT NULL DEFAULT 'X64',
    status VARCHAR(30) NOT NULL DEFAULT 'IDLE',
    labels_json TEXT,
    last_ping_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflows (
    id VARCHAR(36) PRIMARY KEY,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    state VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    yaml_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_repo_workflow_path UNIQUE (repository_id, file_path)
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    id VARCHAR(36) PRIMARY KEY,
    workflow_id VARCHAR(36) NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    repository_id VARCHAR(36) NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
    trigger_user_id VARCHAR(36) REFERENCES users(id),
    run_number INT NOT NULL,
    event VARCHAR(50) NOT NULL,
    head_branch VARCHAR(100) NOT NULL,
    head_sha VARCHAR(64) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'QUEUED',
    conclusion VARCHAR(30),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_workflow_runs_repo ON workflow_runs(repository_id);
CREATE INDEX idx_workflow_runs_status ON workflow_runs(status);

CREATE TABLE IF NOT EXISTS workflow_jobs (
    id VARCHAR(36) PRIMARY KEY,
    run_id VARCHAR(36) NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    runner_id VARCHAR(36) REFERENCES ci_runners(id) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'QUEUED',
    conclusion VARCHAR(30),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS workflow_steps (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL REFERENCES workflow_jobs(id) ON DELETE CASCADE,
    step_number INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'QUEUED',
    conclusion VARCHAR(30),
    logs_storage_path VARCHAR(500),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS ci_artifacts (
    id VARCHAR(36) PRIMARY KEY,
    run_id VARCHAR(36) NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    size_bytes BIGINT NOT NULL,
    storage_path VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""
write_file("backend/src/main/resources/db/migration/V5__create_webhooks_and_ci_cd_engine.sql", v5_sql)

v6_sql = """-- V6: Notifications, Notification Preferences, Outbox Events, and Audit Logs
CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    actor_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    type VARCHAR(50) NOT NULL,
    subject_type VARCHAR(30) NOT NULL,
    subject_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT,
    link_url VARCHAR(500),
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user_unread ON notifications(user_id, is_read);

CREATE TABLE IF NOT EXISTS user_notification_settings (
    user_id VARCHAR(36) PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    email_on_mention BOOLEAN NOT NULL DEFAULT TRUE,
    email_on_assigned BOOLEAN NOT NULL DEFAULT TRUE,
    email_on_review_requested BOOLEAN NOT NULL DEFAULT TRUE,
    email_on_ci_failed BOOLEAN NOT NULL DEFAULT TRUE,
    web_notifications_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS outbox_events (
    id VARCHAR(36) PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(36) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    payload_json TEXT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_outbox_status ON outbox_events(status);

CREATE TABLE IF NOT EXISTS audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    actor_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    organization_id VARCHAR(36) REFERENCES organizations(id) ON DELETE SET NULL,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(36) NOT NULL,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    metadata_json TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_id);
CREATE INDEX idx_audit_logs_org ON audit_logs(organization_id);
CREATE INDEX idx_audit_logs_repo ON audit_logs(repository_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
"""
write_file("backend/src/main/resources/db/migration/V6__create_notifications_and_audit_logs.sql", v6_sql)

v7_sql = """-- V7: Abuse Reports, Moderation, Search Trigram & Fulltext Indexes
CREATE TABLE IF NOT EXISTS abuse_reports (
    id VARCHAR(36) PRIMARY KEY,
    reporter_id VARCHAR(36) NOT NULL REFERENCES users(id),
    target_type VARCHAR(30) NOT NULL,
    target_id VARCHAR(36) NOT NULL,
    reason VARCHAR(100) NOT NULL,
    details TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    resolution_notes TEXT,
    resolved_by_id VARCHAR(36) REFERENCES users(id),
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_abuse_reports_status ON abuse_reports(status);

CREATE TABLE IF NOT EXISTS search_indexes (
    id VARCHAR(36) PRIMARY KEY,
    entity_type VARCHAR(30) NOT NULL,
    entity_id VARCHAR(36) NOT NULL,
    repository_id VARCHAR(36) REFERENCES repositories(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    tags VARCHAR(500),
    language VARCHAR(50),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_search_entity ON search_indexes(entity_type, entity_id);
CREATE INDEX idx_search_repo ON search_indexes(repository_id);
"""
write_file("backend/src/main/resources/db/migration/V7__create_moderation_and_search_indexes.sql", v7_sql)

print("Phase 2 Flyway migrations generated successfully!")
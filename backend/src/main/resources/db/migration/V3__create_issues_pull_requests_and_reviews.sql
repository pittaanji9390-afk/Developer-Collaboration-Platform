-- V3: Issues, Pull Requests, Code Reviews, Inline Comments, Milestones, Labels
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

-- V5: Webhooks, Webhook Deliveries, CI/CD Workflows, Runs, Jobs, Steps, Runners, and Secrets Vault
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

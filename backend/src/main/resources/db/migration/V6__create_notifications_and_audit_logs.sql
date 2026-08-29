-- V6: Notifications, Notification Preferences, Outbox Events, and Audit Logs
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

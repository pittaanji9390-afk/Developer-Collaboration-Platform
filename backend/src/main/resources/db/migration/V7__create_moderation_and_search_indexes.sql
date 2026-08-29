-- V7: Abuse Reports, Moderation, Search Trigram & Fulltext Indexes
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

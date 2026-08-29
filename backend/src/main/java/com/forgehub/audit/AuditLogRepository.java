package com.forgehub.audit;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, String> {
    Page<AuditLog> findByOrganizationIdOrderByCreatedAtDesc(String organizationId, Pageable pageable);
    Page<AuditLog> findByRepositoryIdOrderByCreatedAtDesc(String repositoryId, Pageable pageable);
    Page<AuditLog> findAllByOrderByCreatedAtDesc(Pageable pageable);
}

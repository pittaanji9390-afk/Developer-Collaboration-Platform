from common_writer import write_file

audit_entity = """package com.forgehub.audit;

import com.forgehub.identity.User;
import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "audit_logs")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AuditLog {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actor_id")
    private User actor;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @Column(nullable = false, length = 100)
    private String action;

    @Column(name = "resource_type", nullable = false, length = 50)
    private String resourceType;

    @Column(name = "resource_id", nullable = false)
    private String resourceId;

    @Column(name = "ip_address", length = 45)
    private String ipAddress;

    @Column(name = "user_agent", length = 500)
    private String userAgent;

    @Column(name = "metadata_json", columnDefinition = "TEXT")
    private String metadataJson;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;
}
"""
write_file("backend/src/main/java/com/forgehub/audit/AuditLog.java", audit_entity)

audit_repo = """package com.forgehub.audit;

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
"""
write_file("backend/src/main/java/com/forgehub/audit/AuditLogRepository.java", audit_repo)

abuse_entity = """package com.forgehub.moderation;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "abuse_reports")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AbuseReport {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reporter_id", nullable = false)
    private User reporter;

    @Column(name = "target_type", nullable = false, length = 30)
    private String targetType; // USER, REPOSITORY, ISSUE, COMMENT, DISCUSSION

    @Column(name = "target_id", nullable = false)
    private String targetId;

    @Column(nullable = false, length = 100)
    private String reason;

    @Column(columnDefinition = "TEXT")
    private String details;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private ReportStatus status = ReportStatus.PENDING;

    @Column(name = "resolution_notes", columnDefinition = "TEXT")
    private String resolutionNotes;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "resolved_by_id")
    private User resolvedBy;

    @Column(name = "resolved_at")
    private Instant resolvedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum ReportStatus {
        PENDING, INVESTIGATING, RESOLVED, DISMISSED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/moderation/AbuseReport.java", abuse_entity)

abuse_repo = """package com.forgehub.moderation;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AbuseReportRepository extends JpaRepository<AbuseReport, String> {
    Page<AbuseReport> findByStatusOrderByCreatedAtDesc(AbuseReport.ReportStatus status, Pageable pageable);
}
"""
write_file("backend/src/main/java/com/forgehub/moderation/AbuseReportRepository.java", abuse_repo)

search_entity = """package com.forgehub.search;

import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "search_indexes")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SearchIndex {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @Enumerated(EnumType.STRING)
    @Column(name = "entity_type", nullable = false, length = 30)
    private SearchEntityType entityType;

    @Column(name = "entity_id", nullable = false)
    private String entityId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String content;

    @Column(length = 500)
    private String tags;

    @Column(length = 50)
    private String language;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum SearchEntityType {
        REPOSITORY, ISSUE, PULL_REQUEST, CODE, DISCUSSION, USER
    }
}
"""
write_file("backend/src/main/java/com/forgehub/search/SearchIndex.java", search_entity)

search_repo = """package com.forgehub.search;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface SearchIndexRepository extends JpaRepository<SearchIndex, String> {

    @Query("SELECT s FROM SearchIndex s WHERE LOWER(s.title) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(s.content) LIKE LOWER(CONCAT('%', :query, '%'))")
    Page<SearchIndex> globalSearch(String query, Pageable pageable);

    @Query("SELECT s FROM SearchIndex s WHERE s.entityType = :type AND (LOWER(s.title) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(s.content) LIKE LOWER(CONCAT('%', :query, '%')))")
    Page<SearchIndex> searchByType(SearchIndex.SearchEntityType type, String query, Pageable pageable);
}
"""
write_file("backend/src/main/java/com/forgehub/search/SearchIndexRepository.java", search_repo)

admin_service = """package com.forgehub.administration;

import com.forgehub.identity.UserRepository;
import com.forgehub.organizations.OrganizationRepository;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.workflows.WorkflowRunRepository;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class PlatformAdminService {

    private final UserRepository userRepository;
    private final OrganizationRepository orgRepository;
    private final RepositoryRepository repoRepository;
    private final WorkflowRunRepository workflowRunRepository;

    @Transactional(readOnly = true)
    public PlatformStats getPlatformStats() {
        return PlatformStats.builder()
                .totalUsers(userRepository.count())
                .totalOrganizations(orgRepository.count())
                .totalRepositories(repoRepository.count())
                .totalWorkflowRuns(workflowRunRepository.count())
                .status("HEALTHY")
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PlatformStats {
        private long totalUsers;
        private long totalOrganizations;
        private long totalRepositories;
        private long totalWorkflowRuns;
        private String status;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/administration/PlatformAdminService.java", admin_service)

admin_ctrl = """package com.forgehub.administration;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin")
@RequiredArgsConstructor
@PreAuthorize("hasRole('ADMIN')")
@Tag(name = "Platform Administration", description = "Admin dashboard, metrics, abuse reports and system management")
public class AdminController {

    private final PlatformAdminService adminService;

    @GetMapping("/stats")
    @Operation(summary = "Get global platform statistics")
    public ResponseEntity<ApiResponse<PlatformAdminService.PlatformStats>> getStats() {
        return ResponseEntity.ok(ApiResponse.ok(adminService.getPlatformStats()));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/administration/AdminController.java", admin_ctrl)

print("gen_phase9_platform complete.")
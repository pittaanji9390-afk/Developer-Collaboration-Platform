from common_writer import write_file

webhook_entity = """package com.forgehub.webhooks;

import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "webhooks")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Webhook {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 500)
    private String url;

    @Column(nullable = false)
    private String secret;

    @Column(name = "content_type", nullable = false, length = 30)
    @Builder.Default
    private String contentType = "JSON";

    @Builder.Default
    private boolean active = true;

    @Column(name = "events_json", nullable = false, columnDefinition = "TEXT")
    private String eventsJson;

    @Column(name = "insecure_ssl", nullable = false)
    @Builder.Default
    private boolean insecureSsl = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/webhooks/Webhook.java", webhook_entity)

webhook_delivery = """package com.forgehub.webhooks;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "webhook_deliveries")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WebhookDelivery {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "webhook_id", nullable = false)
    private Webhook webhook;

    @Column(nullable = false, length = 50)
    private String event;

    @Column(name = "delivery_guid", nullable = false, unique = true, length = 64)
    private String deliveryGuid;

    @Column(name = "payload_json", nullable = false, columnDefinition = "TEXT")
    private String payloadJson;

    @Column(name = "request_headers_json", columnDefinition = "TEXT")
    private String requestHeadersJson;

    @Column(name = "response_headers_json", columnDefinition = "TEXT")
    private String responseHeadersJson;

    @Column(name = "response_body", columnDefinition = "TEXT")
    private String responseBody;

    @Column(name = "status_code")
    private Integer statusCode;

    @Column(name = "duration_ms")
    private Long durationMs;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    private DeliveryStatus status;

    @Column(name = "attempts_count", nullable = false)
    @Builder.Default
    private int attemptsCount = 1;

    @Column(name = "next_retry_at")
    private Instant nextRetryAt;

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum DeliveryStatus {
        SUCCESS, FAILED, RETRYING, DEAD_LETTER
    }
}
"""
write_file("backend/src/main/java/com/forgehub/webhooks/WebhookDelivery.java", webhook_delivery)

webhook_repo = """package com.forgehub.webhooks;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WebhookRepository extends JpaRepository<Webhook, String> {
    List<Webhook> findByRepositoryIdAndActiveTrue(String repositoryId);
    List<Webhook> findByOrganizationIdAndActiveTrue(String organizationId);
}
"""
write_file("backend/src/main/java/com/forgehub/webhooks/WebhookRepository.java", webhook_repo)

webhook_deliv_repo = """package com.forgehub.webhooks;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;

@Repository
public interface WebhookDeliveryRepository extends JpaRepository<WebhookDelivery, String> {
    List<WebhookDelivery> findByWebhookIdOrderByCreatedAtDesc(String webhookId);
    List<WebhookDelivery> findByStatusAndNextRetryAtBefore(WebhookDelivery.DeliveryStatus status, Instant now);
}
"""
write_file("backend/src/main/java/com/forgehub/webhooks/WebhookDeliveryRepository.java", webhook_deliv_repo)

secret_entity = """package com.forgehub.secrets;

import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "secrets", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_secret", columnNames = {"repository_id", "name"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SecretEntity {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(name = "encrypted_value", nullable = false, columnDefinition = "TEXT")
    private String encryptedValue;

    @Column(nullable = false, length = 64)
    private String iv;

    @Column(name = "auth_tag", nullable = false, length = 64)
    private String authTag;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/secrets/SecretEntity.java", secret_entity)

workflow_entity = """package com.forgehub.workflows;

import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "workflows", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_workflow_path", columnNames = {"repository_id", "file_path"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Workflow {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(name = "file_path", nullable = false, length = 255)
    private String filePath;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private WorkflowState state = WorkflowState.ACTIVE;

    @Column(name = "yaml_content", nullable = false, columnDefinition = "TEXT")
    private String yamlContent;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum WorkflowState {
        ACTIVE, DISABLED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/Workflow.java", workflow_entity)

workflow_run = """package com.forgehub.workflows;

import com.forgehub.identity.User;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "workflow_runs")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WorkflowRun {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "workflow_id", nullable = false)
    private Workflow workflow;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "trigger_user_id")
    private User triggerUser;

    @Column(name = "run_number", nullable = false)
    private int runNumber;

    @Column(nullable = false, length = 50)
    private String event;

    @Column(name = "head_branch", nullable = false, length = 100)
    private String headBranch;

    @Column(name = "head_sha", nullable = false, length = 64)
    private String headSha;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private RunStatus status = RunStatus.QUEUED;

    @Enumerated(EnumType.STRING)
    @Column(length = 30)
    private RunConclusion conclusion;

    @Column(name = "started_at")
    private Instant startedAt;

    @Column(name = "completed_at")
    private Instant completedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum RunStatus {
        QUEUED, IN_PROGRESS, COMPLETED, CANCELLED
    }

    public enum RunConclusion {
        SUCCESS, FAILURE, CANCELLED, SKIPPED, TIMED_OUT
    }
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowRun.java", workflow_run)

workflow_run_repo = """package com.forgehub.workflows;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WorkflowRunRepository extends JpaRepository<WorkflowRun, String> {
    Page<WorkflowRun> findByRepositoryIdOrderByCreatedAtDesc(String repositoryId, Pageable pageable);
    List<WorkflowRun> findByWorkflowIdOrderByCreatedAtDesc(String workflowId);

    @Query("SELECT COALESCE(MAX(wr.runNumber), 0) + 1 FROM WorkflowRun wr WHERE wr.workflow.id = :workflowId")
    int getNextRunNumber(String workflowId);
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowRunRepository.java", workflow_run_repo)

print("gen_phase8_ci_webhooks complete.")
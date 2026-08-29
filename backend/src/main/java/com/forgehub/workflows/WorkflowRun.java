package com.forgehub.workflows;

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

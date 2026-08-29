package com.forgehub.workflows;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "workflow_steps")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WorkflowStep {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "job_id", nullable = false)
    private WorkflowJob job;

    @Column(name = "step_number", nullable = false)
    private int stepNumber;

    @Column(nullable = false, length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private StepStatus status = StepStatus.QUEUED;

    @Enumerated(EnumType.STRING)
    @Column(length = 30)
    private StepConclusion conclusion;

    @Column(name = "logs_storage_path", length = 500)
    private String logsStoragePath;

    @Column(name = "started_at")
    private Instant startedAt;

    @Column(name = "completed_at")
    private Instant completedAt;

    public enum StepStatus {
        QUEUED, IN_PROGRESS, COMPLETED, CANCELLED
    }

    public enum StepConclusion {
        SUCCESS, FAILURE, SKIPPED
    }
}

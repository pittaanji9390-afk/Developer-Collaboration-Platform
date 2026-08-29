from common_writer import write_file

ci_runner = """package com.forgehub.runners;

import com.forgehub.organizations.Organization;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "ci_runners")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CIRunner {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 100)
    private String token;

    @Column(nullable = false, length = 50)
    @Builder.Default
    private String os = "LINUX";

    @Column(nullable = false, length = 50)
    @Builder.Default
    private String architecture = "X64";

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private RunnerStatus status = RunnerStatus.IDLE;

    @Column(name = "labels_json", columnDefinition = "TEXT")
    private String labelsJson;

    @Column(name = "last_ping_at")
    private Instant lastPingAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum RunnerStatus {
        IDLE, BUSY, OFFLINE
    }
}
"""
write_file("backend/src/main/java/com/forgehub/runners/CIRunner.java", ci_runner)

runner_repo = """package com.forgehub.runners;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface CIRunnerRepository extends JpaRepository<CIRunner, String> {
    Optional<CIRunner> findByToken(String token);
    List<CIRunner> findByStatusAndLastPingAtAfter(CIRunner.RunnerStatus status, Instant pingThreshold);
}
"""
write_file("backend/src/main/java/com/forgehub/runners/CIRunnerRepository.java", runner_repo)

wf_job = """package com.forgehub.workflows;

import com.forgehub.runners.CIRunner;
import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "workflow_jobs")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class WorkflowJob {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "run_id", nullable = false)
    private WorkflowRun run;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "runner_id")
    private CIRunner runner;

    @Column(nullable = false, length = 100)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private JobStatus status = JobStatus.QUEUED;

    @Enumerated(EnumType.STRING)
    @Column(length = 30)
    private JobConclusion conclusion;

    @Column(name = "started_at")
    private Instant startedAt;

    @Column(name = "completed_at")
    private Instant completedAt;

    public enum JobStatus {
        QUEUED, IN_PROGRESS, COMPLETED, CANCELLED
    }

    public enum JobConclusion {
        SUCCESS, FAILURE, CANCELLED, SKIPPED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowJob.java", wf_job)

wf_step = """package com.forgehub.workflows;

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
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowStep.java", wf_step)

job_repo = """package com.forgehub.workflows;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WorkflowJobRepository extends JpaRepository<WorkflowJob, String> {
    List<WorkflowJob> findByRunId(String runId);
    List<WorkflowJob> findByStatus(WorkflowJob.JobStatus status);
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowJobRepository.java", job_repo)

step_repo = """package com.forgehub.workflows;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WorkflowStepRepository extends JpaRepository<WorkflowStep, String> {
    List<WorkflowStep> findByJobIdOrderByStepNumberAsc(String jobId);
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowStepRepository.java", step_repo)

wf_parser = """package com.forgehub.workflows;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class WorkflowYamlParser {

    private final ObjectMapper yamlMapper = new ObjectMapper(new YAMLFactory());

    public ParsedWorkflow parse(String yamlContent) {
        try {
            return yamlMapper.readValue(yamlContent, ParsedWorkflow.class);
        } catch (Exception e) {
            log.error("Failed to parse workflow YAML definition", e);
            throw new IllegalArgumentException("Invalid YAML syntax in workflow file: " + e.getMessage(), e);
        }
    }

    @Data
    public static class ParsedWorkflow {
        private String name;
        private Object on;
        private Map<String, Object> env;
        private Map<String, ParsedJob> jobs;
    }

    @Data
    public static class ParsedJob {
        private String name;
        private String runsOn;
        private List<String> needs;
        private Map<String, String> env;
        private List<ParsedStep> steps;
    }

    @Data
    public static class ParsedStep {
        private String name;
        private String run;
        private String uses;
        private Map<String, String> env;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowYamlParser.java", wf_parser)

wf_engine = """package com.forgehub.workflows;

import com.forgehub.identity.User;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.shared.event.DomainEventPublisher;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class WorkflowEngineService {

    private final WorkflowRunRepository runRepository;
    private final WorkflowJobRepository jobRepository;
    private final WorkflowStepRepository stepRepository;
    private final WorkflowYamlParser yamlParser;
    private final DomainEventPublisher eventPublisher;
    private final SimpMessagingTemplate messagingTemplate;

    @Transactional
    public WorkflowRun triggerWorkflow(Workflow workflow, String event, String branch, String sha, User triggerUser) {
        WorkflowYamlParser.ParsedWorkflow parsed = yamlParser.parse(workflow.getYamlContent());

        int nextRunNumber = runRepository.getNextRunNumber(workflow.getId());

        WorkflowRun run = WorkflowRun.builder()
                .workflow(workflow)
                .repository(workflow.getRepository())
                .triggerUser(triggerUser)
                .runNumber(nextRunNumber)
                .event(event)
                .headBranch(branch)
                .headSha(sha)
                .status(WorkflowRun.RunStatus.IN_PROGRESS)
                .startedAt(Instant.now())
                .build();

        runRepository.save(run);

        if (parsed.getJobs() != null) {
            for (Map.Entry<String, WorkflowYamlParser.ParsedJob> jobEntry : parsed.getJobs().entrySet()) {
                WorkflowYamlParser.ParsedJob parsedJob = jobEntry.getValue();

                WorkflowJob job = WorkflowJob.builder()
                        .run(run)
                        .name(parsedJob.getName() != null ? parsedJob.getName() : jobEntry.getKey())
                        .status(WorkflowJob.JobStatus.QUEUED)
                        .build();

                jobRepository.save(job);

                if (parsedJob.getSteps() != null) {
                    int stepNum = 1;
                    for (WorkflowYamlParser.ParsedStep parsedStep : parsedJob.getSteps()) {
                        WorkflowStep step = WorkflowStep.builder()
                                .job(job)
                                .stepNumber(stepNum++)
                                .name(parsedStep.getName() != null ? parsedStep.getName() : "Step " + (stepNum - 1))
                                .status(WorkflowStep.StepStatus.QUEUED)
                                .build();
                        stepRepository.save(step);
                    }
                }
            }
        }

        eventPublisher.publish("WORKFLOW", run.getId(), "WORKFLOW_RUN_STARTED", run.getId());
        return run;
    }

    public void streamJobLog(String jobId, String logChunk) {
        String topic = "/topic/ci/jobs/" + jobId + "/logs";
        messagingTemplate.convertAndSend(topic, logChunk);
    }
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/WorkflowEngineService.java", wf_engine)

print("build_ci_runner_engine complete.")
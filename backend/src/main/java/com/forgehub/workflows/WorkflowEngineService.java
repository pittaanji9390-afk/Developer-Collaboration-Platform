package com.forgehub.workflows;

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

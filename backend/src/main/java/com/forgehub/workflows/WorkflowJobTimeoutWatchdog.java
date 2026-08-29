package com.forgehub.workflows;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class WorkflowJobTimeoutWatchdog {

    private final WorkflowRunRepository runRepository;
    private final WorkflowJobRepository jobRepository;

    @Scheduled(fixedDelay = 60000)
    @Transactional
    public void checkForTimedOutRuns() {
        Instant timeoutThreshold = Instant.now().minus(60, ChronoUnit.MINUTES);

        List<WorkflowJob> runningJobs = jobRepository.findByStatus(WorkflowJob.JobStatus.IN_PROGRESS);
        for (WorkflowJob job : runningJobs) {
            if (job.getStartedAt() != null && job.getStartedAt().isBefore(timeoutThreshold)) {
                log.warn("Job {} timed out after 60 minutes. Cancelling.", job.getId());
                job.setStatus(WorkflowJob.JobStatus.COMPLETED);
                job.setConclusion(WorkflowJob.JobConclusion.FAILURE);
                job.setCompletedAt(Instant.now());
                jobRepository.save(job);
            }
        }
    }
}

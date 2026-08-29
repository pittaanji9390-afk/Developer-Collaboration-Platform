package com.forgehub.workflows;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WorkflowJobRepository extends JpaRepository<WorkflowJob, String> {
    List<WorkflowJob> findByRunId(String runId);
    List<WorkflowJob> findByStatus(WorkflowJob.JobStatus status);
}

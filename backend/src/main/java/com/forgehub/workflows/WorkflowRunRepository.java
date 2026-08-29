package com.forgehub.workflows;

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

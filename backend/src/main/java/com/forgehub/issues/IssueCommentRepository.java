package com.forgehub.issues;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface IssueCommentRepository extends JpaRepository<IssueComment, String> {
    List<IssueComment> findByIssueIdOrderByCreatedAtAsc(String issueId);
}

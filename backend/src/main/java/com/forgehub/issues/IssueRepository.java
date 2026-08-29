package com.forgehub.issues;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface IssueRepository extends JpaRepository<Issue, String> {
    Optional<Issue> findByRepositoryIdAndNumber(String repositoryId, int number);
    Page<Issue> findByRepositoryIdAndStatus(String repositoryId, Issue.IssueStatus status, Pageable pageable);

    @Query("SELECT COALESCE(MAX(i.number), 0) + 1 FROM Issue i WHERE i.repository.id = :repoId")
    int getNextIssueNumber(String repoId);
}

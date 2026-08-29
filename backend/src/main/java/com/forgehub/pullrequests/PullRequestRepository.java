package com.forgehub.pullrequests;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PullRequestRepository extends JpaRepository<PullRequest, String> {
    Optional<PullRequest> findByRepositoryIdAndNumber(String repositoryId, int number);
    Page<PullRequest> findByRepositoryIdAndStatus(String repositoryId, PullRequest.PRStatus status, Pageable pageable);

    @Query("SELECT COALESCE(MAX(pr.number), 0) + 1 FROM PullRequest pr WHERE pr.repository.id = :repoId")
    int getNextPRNumber(String repoId);
}

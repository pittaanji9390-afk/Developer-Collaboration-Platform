package com.forgehub.pullrequests;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PullRequestReviewRepository extends JpaRepository<PullRequestReview, String> {
    List<PullRequestReview> findByPullRequestId(String pullRequestId);
}

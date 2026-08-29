package com.forgehub.pullrequests;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewThreadRepository extends JpaRepository<ReviewThread, String> {
    List<ReviewThread> findByPullRequestId(String pullRequestId);
}

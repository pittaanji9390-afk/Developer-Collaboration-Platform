package com.forgehub.discussions;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DiscussionCategoryRepository extends JpaRepository<DiscussionCategory, String> {
    List<DiscussionCategory> findByRepositoryId(String repositoryId);
}

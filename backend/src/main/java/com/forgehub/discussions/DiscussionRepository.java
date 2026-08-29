package com.forgehub.discussions;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DiscussionRepository extends JpaRepository<Discussion, String> {
    Page<Discussion> findByRepositoryId(String repositoryId, Pageable pageable);
    Optional<Discussion> findByRepositoryIdAndNumber(String repositoryId, int number);

    @Query("SELECT COALESCE(MAX(d.number), 0) + 1 FROM Discussion d WHERE d.repository.id = :repoId")
    int getNextDiscussionNumber(String repoId);
}

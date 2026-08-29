package com.forgehub.repositories;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface RepositoryRepository extends JpaRepository<RepositoryEntity, String> {
    Optional<RepositoryEntity> findByOwnerUserUsernameAndSlug(String username, String slug);
    Optional<RepositoryEntity> findByOrganizationSlugAndSlug(String orgSlug, String slug);

    Page<RepositoryEntity> findByOwnerUserUsername(String username, Pageable pageable);
    Page<RepositoryEntity> findByOrganizationSlug(String orgSlug, Pageable pageable);
    Page<RepositoryEntity> findByVisibility(RepositoryEntity.RepoVisibility visibility, Pageable pageable);

    @Query("SELECT r FROM RepositoryEntity r WHERE r.visibility = 'PUBLIC' AND (LOWER(r.name) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(r.description) LIKE LOWER(CONCAT('%', :query, '%')))")
    Page<RepositoryEntity> searchPublic(String query, Pageable pageable);
}

from common_writer import write_file

repo_entity = """package com.forgehub.repositories;

import com.forgehub.identity.User;
import com.forgehub.organizations.Organization;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "repositories")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RepositoryEntity {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "owner_user_id")
    private User ownerUser;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 100)
    private String slug;

    @Column(length = 1000)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private RepoVisibility visibility = RepoVisibility.PUBLIC;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private RepoStatus status = RepoStatus.ACTIVE;

    @Column(name = "default_branch", nullable = false, length = 100)
    @Builder.Default
    private String defaultBranch = "main";

    @Column(name = "repository_path", nullable = false, length = 500)
    private String repositoryPath;

    @Column(name = "size_bytes", nullable = false)
    @Builder.Default
    private long sizeBytes = 0;

    @Column(name = "fork_count", nullable = false)
    @Builder.Default
    private int forkCount = 0;

    @Column(name = "star_count", nullable = false)
    @Builder.Default
    private int starCount = 0;

    @Column(name = "watch_count", nullable = false)
    @Builder.Default
    private int watchCount = 0;

    @Column(name = "open_issues_count", nullable = false)
    @Builder.Default
    private int openIssuesCount = 0;

    @Column(name = "open_prs_count", nullable = false)
    @Builder.Default
    private int openPrsCount = 0;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_repository_id")
    private RepositoryEntity parentRepository;

    @Column(name = "allow_forking", nullable = false)
    @Builder.Default
    private boolean allowForking = true;

    @Column(name = "allow_merge_commit", nullable = false)
    @Builder.Default
    private boolean allowMergeCommit = true;

    @Column(name = "allow_squash_merge", nullable = false)
    @Builder.Default
    private boolean allowSquashMerge = true;

    @Column(name = "allow_rebase_merge", nullable = false)
    @Builder.Default
    private boolean allowRebaseMerge = true;

    @Column(name = "delete_branch_on_merge", nullable = false)
    @Builder.Default
    private boolean deleteBranchOnMerge = false;

    @Column(name = "has_issues", nullable = false)
    @Builder.Default
    private boolean hasIssues = true;

    @Column(name = "has_projects", nullable = false)
    @Builder.Default
    private boolean hasProjects = true;

    @Column(name = "has_discussions", nullable = false)
    @Builder.Default
    private boolean hasDiscussions = true;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Column(name = "archived_at")
    private Instant archivedAt;

    public enum RepoVisibility {
        PUBLIC, PRIVATE, INTERNAL
    }

    public enum RepoStatus {
        ACTIVE, ARCHIVED, SUSPENDED, DELETED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/repositories/RepositoryEntity.java", repo_entity)

collab_entity = """package com.forgehub.repositories;

import com.forgehub.authorization.PermissionLevel;
import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "repository_collaborators", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_collaborator", columnNames = {"repository_id", "user_id"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Collaborator {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private PermissionLevel permission = PermissionLevel.WRITE;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/repositories/Collaborator.java", collab_entity)

collab_repo = """package com.forgehub.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CollaboratorRepository extends JpaRepository<Collaborator, String> {
    Optional<Collaborator> findByRepositoryIdAndUserId(String repositoryId, String userId);
    List<Collaborator> findByRepositoryId(String repositoryId);
}
"""
write_file("backend/src/main/java/com/forgehub/repositories/CollaboratorRepository.java", collab_repo)

repo_repo = """package com.forgehub.repositories;

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
"""
write_file("backend/src/main/java/com/forgehub/repositories/RepositoryRepository.java", repo_repo)

print("gen_phase5_repos complete.")
package com.forgehub.pullrequests;

import com.forgehub.identity.User;
import com.forgehub.issues.Milestone;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "pull_requests", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_pr_num", columnNames = {"repository_id", "number"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PullRequest {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @Column(nullable = false)
    private int number;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String body;

    @Column(name = "source_branch", nullable = false, length = 100)
    private String sourceBranch;

    @Column(name = "target_branch", nullable = false, length = 100)
    private String targetBranch;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_repository_id")
    private RepositoryEntity sourceRepository;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private PRStatus status = PRStatus.OPEN;

    @Builder.Default
    private boolean draft = false;

    @Builder.Default
    private boolean mergeable = true;

    @Enumerated(EnumType.STRING)
    @Column(name = "merge_strategy", length = 30)
    private MergeStrategy mergeStrategy;

    @Column(name = "merged_at")
    private Instant mergedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "merged_by_id")
    private User mergedBy;

    @Column(name = "closed_at")
    private Instant closedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "closed_by_id")
    private User closedBy;

    @Column(name = "base_commit_sha", length = 64)
    private String baseCommitSha;

    @Column(name = "head_commit_sha", length = 64)
    private String headCommitSha;

    @Column(name = "merge_commit_sha", length = 64)
    private String mergeCommitSha;

    @Column(name = "additions_count", nullable = false)
    @Builder.Default
    private int additionsCount = 0;

    @Column(name = "deletions_count", nullable = false)
    @Builder.Default
    private int deletionsCount = 0;

    @Column(name = "changed_files_count", nullable = false)
    @Builder.Default
    private int changedFilesCount = 0;

    @Column(name = "comments_count", nullable = false)
    @Builder.Default
    private int commentsCount = 0;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum PRStatus {
        OPEN, CLOSED, MERGED
    }

    public enum MergeStrategy {
        MERGE_COMMIT, SQUASH, REBASE
    }
}

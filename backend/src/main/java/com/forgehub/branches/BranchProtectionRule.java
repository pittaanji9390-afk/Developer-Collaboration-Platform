package com.forgehub.branches;

import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "branch_protection_rules", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_branch_rule", columnNames = {"repository_id", "branch_pattern"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BranchProtectionRule {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @Column(name = "branch_pattern", nullable = false, length = 100)
    private String branchPattern; // e.g. "main", "release/*"

    @Column(name = "require_pull_request", nullable = false)
    @Builder.Default
    private boolean requirePullRequest = true;

    @Column(name = "required_approving_review_count", nullable = false)
    @Builder.Default
    private int requiredApprovingReviewCount = 1;

    @Column(name = "dismiss_stale_reviews", nullable = false)
    @Builder.Default
    private boolean dismissStaleReviews = false;

    @Column(name = "require_code_owner_reviews", nullable = false)
    @Builder.Default
    private boolean requireCodeOwnerReviews = false;

    @Column(name = "require_status_checks", nullable = false)
    @Builder.Default
    private boolean requireStatusChecks = false;

    @Column(name = "required_status_checks_json", columnDefinition = "TEXT")
    private String requiredStatusChecksJson;

    @Column(name = "require_conversation_resolution", nullable = false)
    @Builder.Default
    private boolean requireConversationResolution = true;

    @Column(name = "require_signed_commits", nullable = false)
    @Builder.Default
    private boolean requireSignedCommits = false;

    @Column(name = "require_linear_history", nullable = false)
    @Builder.Default
    private boolean requireLinearHistory = false;

    @Column(name = "allow_force_pushes", nullable = false)
    @Builder.Default
    private boolean allowForcePushes = false;

    @Column(name = "allow_deletions", nullable = false)
    @Builder.Default
    private boolean allowDeletions = false;

    @Column(name = "block_creations", nullable = false)
    @Builder.Default
    private boolean blockCreations = false;

    @Column(name = "enforce_admins", nullable = false)
    @Builder.Default
    private boolean enforceAdmins = true;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}

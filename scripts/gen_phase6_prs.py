from common_writer import write_file

pr_entity = """package com.forgehub.pullrequests;

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
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/PullRequest.java", pr_entity)

pr_review = """package com.forgehub.pullrequests;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "pull_request_reviews")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PullRequestReview {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pull_request_id", nullable = false)
    private PullRequest pullRequest;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @Column(name = "commit_sha", nullable = false, length = 64)
    private String commitSha;

    @Column(columnDefinition = "TEXT")
    private String body;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private ReviewState state = ReviewState.PENDING;

    @Column(name = "submitted_at")
    private Instant submittedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum ReviewState {
        PENDING, COMMENTED, APPROVED, CHANGES_REQUESTED, DISMISSED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/PullRequestReview.java", pr_review)

review_thread = """package com.forgehub.pullrequests;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "review_threads")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReviewThread {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pull_request_id", nullable = false)
    private PullRequest pullRequest;

    @Column(name = "file_path", nullable = false, length = 500)
    private String filePath;

    @Column(name = "line_number", nullable = false)
    private int lineNumber;

    @Column(nullable = false, length = 10)
    @Builder.Default
    private String side = "RIGHT";

    @Column(name = "commit_sha", nullable = false, length = 64)
    private String commitSha;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private ThreadStatus status = ThreadStatus.OPEN;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "resolved_by_id")
    private User resolvedBy;

    @Column(name = "resolved_at")
    private Instant resolvedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum ThreadStatus {
        OPEN, RESOLVED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/ReviewThread.java", review_thread)

review_comment = """package com.forgehub.pullrequests;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "review_comments")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReviewComment {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "thread_id", nullable = false)
    private ReviewThread thread;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "review_id")
    private PullRequestReview review;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String body;

    @Column(name = "diff_hunk", columnDefinition = "TEXT")
    private String diffHunk;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/ReviewComment.java", review_comment)

pr_repo = """package com.forgehub.pullrequests;

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
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/PullRequestRepository.java", pr_repo)

pr_service = """package com.forgehub.pullrequests;

import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.dto.PageResponse;
import com.forgehub.shared.event.DomainEventPublisher;
import com.forgehub.shared.exception.ApiException;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class PullRequestService {

    private final PullRequestRepository prRepository;
    private final RepositoryRepository repoRepository;
    private final UserRepository userRepository;
    private final DomainEventPublisher eventPublisher;

    @Transactional
    public PRResponse createPullRequest(String userId, String repoId, CreatePRRequest req) {
        User author = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        int nextNum = prRepository.getNextPRNumber(repoId);

        PullRequest pr = PullRequest.builder()
                .repository(repo)
                .author(author)
                .number(nextNum)
                .title(req.getTitle())
                .body(req.getBody())
                .sourceBranch(req.getSourceBranch())
                .targetBranch(req.getTargetBranch())
                .status(PullRequest.PRStatus.OPEN)
                .draft(req.isDraft())
                .mergeable(true)
                .build();

        prRepository.save(pr);
        repo.setOpenPrsCount(repo.getOpenPrsCount() + 1);
        repoRepository.save(repo);

        eventPublisher.publish("PULL_REQUEST", pr.getId(), "PR_OPENED", toResponse(pr));

        return toResponse(pr);
    }

    @Transactional(readOnly = true)
    public PRResponse getPullRequest(String repoId, int number) {
        PullRequest pr = prRepository.findByRepositoryIdAndNumber(repoId, number)
                .orElseThrow(() -> ApiException.notFound("Pull Request #" + number + " not found"));
        return toResponse(pr);
    }

    @Transactional(readOnly = true)
    public PageResponse<PRResponse> listPullRequests(String repoId, PullRequest.PRStatus status, Pageable pageable) {
        Page<PRResponse> page = prRepository.findByRepositoryIdAndStatus(repoId, status, pageable)
                .map(this::toResponse);
        return PageResponse.from(page);
    }

    @Transactional
    public PRResponse mergePullRequest(String userId, String repoId, int number, PullRequest.MergeStrategy strategy) {
        User merger = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));
        PullRequest pr = prRepository.findByRepositoryIdAndNumber(repoId, number)
                .orElseThrow(() -> ApiException.notFound("Pull Request not found"));

        if (pr.getStatus() != PullRequest.PRStatus.OPEN) {
            throw ApiException.badRequest("Pull Request is not open");
        }

        pr.setStatus(PullRequest.PRStatus.MERGED);
        pr.setMergeStrategy(strategy != null ? strategy : PullRequest.MergeStrategy.MERGE_COMMIT);
        pr.setMergedAt(Instant.now());
        pr.setMergedBy(merger);

        prRepository.save(pr);

        RepositoryEntity repo = pr.getRepository();
        repo.setOpenPrsCount(Math.max(0, repo.getOpenPrsCount() - 1));
        repoRepository.save(repo);

        eventPublisher.publish("PULL_REQUEST", pr.getId(), "PR_MERGED", toResponse(pr));

        return toResponse(pr);
    }

    private PRResponse toResponse(PullRequest pr) {
        return PRResponse.builder()
                .id(pr.getId())
                .number(pr.getNumber())
                .title(pr.getTitle())
                .body(pr.getBody())
                .sourceBranch(pr.getSourceBranch())
                .targetBranch(pr.getTargetBranch())
                .status(pr.getStatus().name())
                .draft(pr.isDraft())
                .mergeable(pr.isMergeable())
                .authorUsername(pr.getAuthor().getUsername())
                .authorAvatarUrl(pr.getAuthor().getAvatarUrl())
                .additions(pr.getAdditionsCount())
                .deletions(pr.getDeletionsCount())
                .changedFiles(pr.getChangedFilesCount())
                .createdAt(pr.getCreatedAt())
                .updatedAt(pr.getUpdatedAt())
                .mergedAt(pr.getMergedAt())
                .build();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreatePRRequest {
        @NotBlank
        private String title;
        private String body;
        @NotBlank
        private String sourceBranch;
        @NotBlank
        private String targetBranch;
        private boolean draft;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PRResponse {
        private String id;
        private int number;
        private String title;
        private String body;
        private String sourceBranch;
        private String targetBranch;
        private String status;
        private boolean draft;
        private boolean mergeable;
        private String authorUsername;
        private String authorAvatarUrl;
        private int additions;
        private int deletions;
        private int changedFiles;
        private Instant createdAt;
        private Instant updatedAt;
        private Instant mergedAt;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/PullRequestService.java", pr_service)

pr_ctrl = """package com.forgehub.pullrequests;

import com.forgehub.identity.UserPrincipal;
import com.forgehub.shared.dto.ApiResponse;
import com.forgehub.shared.dto.PageResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/repositories/{repoId}/pulls")
@RequiredArgsConstructor
@Tag(name = "Pull Requests", description = "Code comparison, pull requests, reviews and merging")
public class PullRequestController {

    private final PullRequestService prService;

    @PostMapping
    @Operation(summary = "Create a new pull request")
    public ResponseEntity<ApiResponse<PullRequestService.PRResponse>> createPullRequest(
            @AuthenticationPrincipal UserPrincipal principal,
            @PathVariable String repoId,
            @Valid @RequestBody PullRequestService.CreatePRRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Pull request opened", prService.createPullRequest(principal.getId(), repoId, request)));
    }

    @GetMapping("/{number}")
    @Operation(summary = "Get pull request details by number")
    public ResponseEntity<ApiResponse<PullRequestService.PRResponse>> getPullRequest(
            @PathVariable String repoId,
            @PathVariable int number
    ) {
        return ResponseEntity.ok(ApiResponse.ok(prService.getPullRequest(repoId, number)));
    }

    @GetMapping
    @Operation(summary = "List pull requests in repository")
    public ResponseEntity<ApiResponse<PageResponse<PullRequestService.PRResponse>>> listPullRequests(
            @PathVariable String repoId,
            @RequestParam(defaultValue = "OPEN") PullRequest.PRStatus status,
            @PageableDefault(size = 25) Pageable pageable
    ) {
        return ResponseEntity.ok(ApiResponse.ok(prService.listPullRequests(repoId, status, pageable)));
    }

    @PostMapping("/{number}/merge")
    @Operation(summary = "Merge pull request")
    public ResponseEntity<ApiResponse<PullRequestService.PRResponse>> mergePullRequest(
            @AuthenticationPrincipal UserPrincipal principal,
            @PathVariable String repoId,
            @PathVariable int number,
            @RequestParam(defaultValue = "MERGE_COMMIT") PullRequest.MergeStrategy strategy
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Pull request merged", prService.mergePullRequest(principal.getId(), repoId, number, strategy)));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/PullRequestController.java", pr_ctrl)

print("gen_phase6_prs complete.")
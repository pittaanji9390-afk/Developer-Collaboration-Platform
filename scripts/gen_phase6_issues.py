from common_writer import write_file

issue_entity = """package com.forgehub.issues;

import com.forgehub.identity.User;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "issues", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_issue_num", columnNames = {"repository_id", "number"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Issue {

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

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private IssueStatus status = IssueStatus.OPEN;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private IssuePriority priority = IssuePriority.MEDIUM;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "milestone_id")
    private Milestone milestone;

    @Builder.Default
    private boolean locked = false;

    @Column(name = "comments_count", nullable = false)
    @Builder.Default
    private int commentsCount = 0;

    @ManyToMany
    @JoinTable(
            name = "issue_assignees",
            joinColumns = @JoinColumn(name = "issue_id"),
            inverseJoinColumns = @JoinColumn(name = "user_id")
    )
    @Builder.Default
    private Set<User> assignees = new HashSet<>();

    @ManyToMany
    @JoinTable(
            name = "issue_label_assignments",
            joinColumns = @JoinColumn(name = "issue_id"),
            inverseJoinColumns = @JoinColumn(name = "label_id")
    )
    @Builder.Default
    private Set<Label> labels = new HashSet<>();

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Column(name = "closed_at")
    private Instant closedAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "closed_by_id")
    private User closedBy;

    public enum IssueStatus {
        OPEN, CLOSED
    }

    public enum IssuePriority {
        LOW, MEDIUM, HIGH, URGENT
    }
}
"""
write_file("backend/src/main/java/com/forgehub/issues/Issue.java", issue_entity)

label_entity = """package com.forgehub.issues;

import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "labels")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Label {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 20)
    @Builder.Default
    private String color = "#0284c7";

    @Column(length = 255)
    private String description;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;
}
"""
write_file("backend/src/main/java/com/forgehub/issues/Label.java", label_entity)

milestone_entity = """package com.forgehub.issues;

import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "milestones")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Milestone {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private MilestoneState state = MilestoneState.OPEN;

    @Column(name = "due_date")
    private Instant dueDate;

    @Column(name = "closed_at")
    private Instant closedAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum MilestoneState {
        OPEN, CLOSED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/issues/Milestone.java", milestone_entity)

issue_comment = """package com.forgehub.issues;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "issue_comments")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class IssueComment {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "issue_id", nullable = false)
    private Issue issue;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String body;

    @Builder.Default
    private boolean edited = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/issues/IssueComment.java", issue_comment)

issue_repo = """package com.forgehub.issues;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface IssueRepository extends JpaRepository<Issue, String> {
    Optional<Issue> findByRepositoryIdAndNumber(String repositoryId, int number);
    Page<Issue> findByRepositoryIdAndStatus(String repositoryId, Issue.IssueStatus status, Pageable pageable);

    @Query("SELECT COALESCE(MAX(i.number), 0) + 1 FROM Issue i WHERE i.repository.id = :repoId")
    int getNextIssueNumber(String repoId);
}
"""
write_file("backend/src/main/java/com/forgehub/issues/IssueRepository.java", issue_repo)

issue_comment_repo = """package com.forgehub.issues;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface IssueCommentRepository extends JpaRepository<IssueComment, String> {
    List<IssueComment> findByIssueIdOrderByCreatedAtAsc(String issueId);
}
"""
write_file("backend/src/main/java/com/forgehub/issues/IssueCommentRepository.java", issue_comment_repo)

issue_service = """package com.forgehub.issues;

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
import java.util.List;

@Service
@RequiredArgsConstructor
public class IssueService {

    private final IssueRepository issueRepository;
    private final IssueCommentRepository commentRepository;
    private final RepositoryRepository repoRepository;
    private final UserRepository userRepository;
    private final DomainEventPublisher eventPublisher;

    @Transactional
    public IssueResponse createIssue(String userId, String repoId, CreateIssueRequest req) {
        User author = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        int nextNumber = issueRepository.getNextIssueNumber(repoId);

        Issue issue = Issue.builder()
                .repository(repo)
                .author(author)
                .number(nextNumber)
                .title(req.getTitle())
                .body(req.getBody())
                .status(Issue.IssueStatus.OPEN)
                .priority(req.getPriority() != null ? req.getPriority() : Issue.IssuePriority.MEDIUM)
                .build();

        issueRepository.save(issue);
        repo.setOpenIssuesCount(repo.getOpenIssuesCount() + 1);
        repoRepository.save(repo);

        eventPublisher.publish("ISSUE", issue.getId(), "ISSUE_CREATED", toResponse(issue));

        return toResponse(issue);
    }

    @Transactional(readOnly = true)
    public IssueResponse getIssue(String repoId, int number) {
        Issue issue = issueRepository.findByRepositoryIdAndNumber(repoId, number)
                .orElseThrow(() -> ApiException.notFound("Issue #" + number + " not found"));
        return toResponse(issue);
    }

    @Transactional(readOnly = true)
    public PageResponse<IssueResponse> listIssues(String repoId, Issue.IssueStatus status, Pageable pageable) {
        Page<IssueResponse> page = issueRepository.findByRepositoryIdAndStatus(repoId, status, pageable)
                .map(this::toResponse);
        return PageResponse.from(page);
    }

    @Transactional
    public CommentResponse addComment(String userId, String issueId, String body) {
        User author = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));
        Issue issue = issueRepository.findById(issueId)
                .orElseThrow(() -> ApiException.notFound("Issue not found"));

        IssueComment comment = IssueComment.builder()
                .issue(issue)
                .author(author)
                .body(body)
                .build();

        commentRepository.save(comment);
        issue.setCommentsCount(issue.getCommentsCount() + 1);
        issueRepository.save(issue);

        eventPublisher.publish("ISSUE", issue.getId(), "COMMENT_ADDED", comment.getId());

        return CommentResponse.builder()
                .id(comment.getId())
                .authorUsername(author.getUsername())
                .authorAvatarUrl(author.getAvatarUrl())
                .body(comment.getBody())
                .createdAt(comment.getCreatedAt())
                .build();
    }

    private IssueResponse toResponse(Issue i) {
        return IssueResponse.builder()
                .id(i.getId())
                .number(i.getNumber())
                .title(i.getTitle())
                .body(i.getBody())
                .status(i.getStatus().name())
                .priority(i.getPriority().name())
                .authorUsername(i.getAuthor().getUsername())
                .authorAvatarUrl(i.getAuthor().getAvatarUrl())
                .commentsCount(i.getCommentsCount())
                .createdAt(i.getCreatedAt())
                .updatedAt(i.getUpdatedAt())
                .closedAt(i.getClosedAt())
                .build();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateIssueRequest {
        @NotBlank
        private String title;
        private String body;
        private Issue.IssuePriority priority;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class IssueResponse {
        private String id;
        private int number;
        private String title;
        private String body;
        private String status;
        private String priority;
        private String authorUsername;
        private String authorAvatarUrl;
        private int commentsCount;
        private Instant createdAt;
        private Instant updatedAt;
        private Instant closedAt;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CommentResponse {
        private String id;
        private String authorUsername;
        private String authorAvatarUrl;
        private String body;
        private Instant createdAt;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/issues/IssueService.java", issue_service)

issue_ctrl = """package com.forgehub.issues;

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
@RequestMapping("/api/v1/repositories/{repoId}/issues")
@RequiredArgsConstructor
@Tag(name = "Issues", description = "Issue tracker, labels, milestones and discussions")
public class IssueController {

    private final IssueService issueService;

    @PostMapping
    @Operation(summary = "Open a new issue in repository")
    public ResponseEntity<ApiResponse<IssueService.IssueResponse>> createIssue(
            @AuthenticationPrincipal UserPrincipal principal,
            @PathVariable String repoId,
            @Valid @RequestBody IssueService.CreateIssueRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Issue created", issueService.createIssue(principal.getId(), repoId, request)));
    }

    @GetMapping("/{number}")
    @Operation(summary = "Get issue details by issue number")
    public ResponseEntity<ApiResponse<IssueService.IssueResponse>> getIssue(
            @PathVariable String repoId,
            @PathVariable int number
    ) {
        return ResponseEntity.ok(ApiResponse.ok(issueService.getIssue(repoId, number)));
    }

    @GetMapping
    @Operation(summary = "List issues in repository with filtering")
    public ResponseEntity<ApiResponse<PageResponse<IssueService.IssueResponse>>> listIssues(
            @PathVariable String repoId,
            @RequestParam(defaultValue = "OPEN") Issue.IssueStatus status,
            @PageableDefault(size = 25) Pageable pageable
    ) {
        return ResponseEntity.ok(ApiResponse.ok(issueService.listIssues(repoId, status, pageable)));
    }

    @PostMapping("/{issueId}/comments")
    @Operation(summary = "Add a comment to an issue")
    public ResponseEntity<ApiResponse<IssueService.CommentResponse>> addComment(
            @AuthenticationPrincipal UserPrincipal principal,
            @PathVariable String issueId,
            @RequestBody String body
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Comment posted", issueService.addComment(principal.getId(), issueId, body)));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/issues/IssueController.java", issue_ctrl)

print("gen_phase6_issues complete.")
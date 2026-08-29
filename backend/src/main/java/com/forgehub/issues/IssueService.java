package com.forgehub.issues;

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

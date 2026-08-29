package com.forgehub.pullrequests;

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

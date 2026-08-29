package com.forgehub.discussions;

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
public class DiscussionService {

    private final DiscussionRepository discussionRepository;
    private final DiscussionCategoryRepository categoryRepository;
    private final RepositoryRepository repoRepository;
    private final UserRepository userRepository;
    private final DomainEventPublisher eventPublisher;

    @Transactional
    public DiscussionResponse createDiscussion(String userId, String repoId, CreateDiscussionRequest req) {
        User author = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));
        DiscussionCategory cat = categoryRepository.findById(req.getCategoryId())
                .orElseThrow(() -> ApiException.notFound("Category not found"));

        int nextNum = discussionRepository.getNextDiscussionNumber(repoId);

        Discussion disc = Discussion.builder()
                .repository(repo)
                .category(cat)
                .author(author)
                .number(nextNum)
                .title(req.getTitle())
                .body(req.getBody())
                .build();

        discussionRepository.save(disc);

        eventPublisher.publish("DISCUSSION", disc.getId(), "DISCUSSION_CREATED", toResponse(disc));

        return toResponse(disc);
    }

    @Transactional(readOnly = true)
    public PageResponse<DiscussionResponse> listDiscussions(String repoId, Pageable pageable) {
        Page<DiscussionResponse> page = discussionRepository.findByRepositoryId(repoId, pageable)
                .map(this::toResponse);
        return PageResponse.from(page);
    }

    private DiscussionResponse toResponse(Discussion d) {
        return DiscussionResponse.builder()
                .id(d.getId())
                .number(d.getNumber())
                .title(d.getTitle())
                .body(d.getBody())
                .categoryName(d.getCategory().getName())
                .categoryEmoji(d.getCategory().getEmoji())
                .authorUsername(d.getAuthor().getUsername())
                .authorAvatarUrl(d.getAuthor().getAvatarUrl())
                .commentsCount(d.getCommentsCount())
                .upvotesCount(d.getUpvotesCount())
                .locked(d.isLocked())
                .pinned(d.isPinned())
                .createdAt(d.getCreatedAt())
                .updatedAt(d.getUpdatedAt())
                .build();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateDiscussionRequest {
        @NotBlank
        private String categoryId;
        @NotBlank
        private String title;
        @NotBlank
        private String body;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DiscussionResponse {
        private String id;
        private int number;
        private String title;
        private String body;
        private String categoryName;
        private String categoryEmoji;
        private String authorUsername;
        private String authorAvatarUrl;
        private int commentsCount;
        private int upvotesCount;
        private boolean locked;
        private boolean pinned;
        private Instant createdAt;
        private Instant updatedAt;
    }
}

from common_writer import write_file

# 1. Tags & Releases
tag_svc = """package com.forgehub.tags;

import com.forgehub.git.GitDTOs;
import com.forgehub.git.JGitService;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.RequiredArgsConstructor;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.lib.Ref;
import org.eclipse.jgit.lib.Repository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class TagService {

    private final RepositoryRepository repoRepository;
    private final JGitService gitService;

    public List<TagResponse> listTags(String repoId) {
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        List<TagResponse> result = new ArrayList<>();
        try (Repository repository = gitService.openRepository(repo.getRepositoryPath());
             Git git = new Git(repository)) {

            List<Ref> tagRefs = git.tagList().call();
            for (Ref ref : tagRefs) {
                String name = ref.getName().replace("refs/tags/", "");
                result.add(new TagResponse(name, ref.getObjectId().name()));
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to list Git tags", e);
        }
        return result;
    }

    public record TagResponse(String name, String commitSha) {}
}
"""
write_file("backend/src/main/java/com/forgehub/tags/TagService.java", tag_svc)

tag_ctrl = """package com.forgehub.tags;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/repositories/{repoId}/tags")
@RequiredArgsConstructor
@Tag(name = "Tags", description = "Git tag operations and browsing")
public class TagController {

    private final TagService tagService;

    @GetMapping
    @Operation(summary = "List Git tags in repository")
    public ResponseEntity<ApiResponse<List<TagService.TagResponse>>> listTags(@PathVariable String repoId) {
        return ResponseEntity.ok(ApiResponse.ok(tagService.listTags(repoId)));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/tags/TagController.java", tag_ctrl)

# 2. Discussions Service & Controller
disc_svc = """package com.forgehub.discussions;

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
"""
write_file("backend/src/main/java/com/forgehub/discussions/DiscussionService.java", disc_svc)

disc_cat_repo = """package com.forgehub.discussions;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DiscussionCategoryRepository extends JpaRepository<DiscussionCategory, String> {
    List<DiscussionCategory> findByRepositoryId(String repositoryId);
}
"""
write_file("backend/src/main/java/com/forgehub/discussions/DiscussionCategoryRepository.java", disc_cat_repo)

disc_ctrl = """package com.forgehub.discussions;

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
@RequestMapping("/api/v1/repositories/{repoId}/discussions")
@RequiredArgsConstructor
@Tag(name = "Discussions", description = "Repository community discussions and Q&A")
public class DiscussionController {

    private final DiscussionService discussionService;

    @PostMapping
    @Operation(summary = "Create a discussion topic")
    public ResponseEntity<ApiResponse<DiscussionService.DiscussionResponse>> createDiscussion(
            @AuthenticationPrincipal UserPrincipal principal,
            @PathVariable String repoId,
            @Valid @RequestBody DiscussionService.CreateDiscussionRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Discussion opened", discussionService.createDiscussion(principal.getId(), repoId, request)));
    }

    @GetMapping
    @Operation(summary = "List discussions with pagination")
    public ResponseEntity<ApiResponse<PageResponse<DiscussionService.DiscussionResponse>>> listDiscussions(
            @PathVariable String repoId,
            @PageableDefault(size = 20) Pageable pageable
    ) {
        return ResponseEntity.ok(ApiResponse.ok(discussionService.listDiscussions(repoId, pageable)));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/discussions/DiscussionController.java", disc_ctrl)

print("gen_full_services complete.")
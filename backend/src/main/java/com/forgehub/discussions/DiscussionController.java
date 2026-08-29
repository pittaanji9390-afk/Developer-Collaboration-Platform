package com.forgehub.discussions;

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

package com.forgehub.pullrequests;

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

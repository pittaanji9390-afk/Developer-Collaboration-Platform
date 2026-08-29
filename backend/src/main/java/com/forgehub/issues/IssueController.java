package com.forgehub.issues;

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

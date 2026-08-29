package com.forgehub.repositories;

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
@RequestMapping("/api/v1/repositories")
@RequiredArgsConstructor
@Tag(name = "Repositories", description = "Repository creation, settings, and browsing")
public class RepositoryController {

    private final RepositoryService repoService;

    @PostMapping
    @Operation(summary = "Create a new Git repository")
    public ResponseEntity<ApiResponse<RepositoryService.RepoResponse>> createRepository(
            @AuthenticationPrincipal UserPrincipal principal,
            @Valid @RequestBody RepositoryService.CreateRepoRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Repository created", repoService.createRepository(principal.getId(), request)));
    }

    @GetMapping("/{owner}/{slug}")
    @Operation(summary = "Get repository metadata by owner and slug")
    public ResponseEntity<ApiResponse<RepositoryService.RepoResponse>> getRepository(
            @PathVariable String owner,
            @PathVariable String slug
    ) {
        return ResponseEntity.ok(ApiResponse.ok(repoService.getRepository(owner, slug)));
    }

    @GetMapping
    @Operation(summary = "List public repositories with pagination")
    public ResponseEntity<ApiResponse<PageResponse<RepositoryService.RepoResponse>>> listRepositories(
            @PageableDefault(size = 20) Pageable pageable
    ) {
        return ResponseEntity.ok(ApiResponse.ok(repoService.listPublicRepositories(pageable)));
    }
}

package com.forgehub.git;

import com.forgehub.git.GitDTOs.*;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.dto.ApiResponse;
import com.forgehub.shared.exception.ApiException;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/repositories/{repoId}/git")
@RequiredArgsConstructor
@Tag(name = "Git Operations", description = "Low-level Git objects, trees, commits, diffs and blame")
public class GitController {

    private final JGitService gitService;
    private final RepositoryRepository repoRepository;

    @GetMapping("/tree")
    @Operation(summary = "Explore repository tree hierarchy")
    public ResponseEntity<ApiResponse<List<GitTreeEntry>>> getTree(
            @PathVariable String repoId,
            @RequestParam(defaultValue = "main") String ref,
            @RequestParam(required = false) String path
    ) {
        RepositoryEntity repo = getRepo(repoId);
        return ResponseEntity.ok(ApiResponse.ok(gitService.listTree(repo.getRepositoryPath(), ref, path)));
    }

    @GetMapping("/blob")
    @Operation(summary = "Get file contents and metadata")
    public ResponseEntity<ApiResponse<GitBlob>> getBlob(
            @PathVariable String repoId,
            @RequestParam(defaultValue = "main") String ref,
            @RequestParam String path
    ) {
        RepositoryEntity repo = getRepo(repoId);
        return ResponseEntity.ok(ApiResponse.ok(gitService.getBlob(repo.getRepositoryPath(), ref, path)));
    }

    @GetMapping("/commits")
    @Operation(summary = "Get commit history walk")
    public ResponseEntity<ApiResponse<List<GitCommit>>> getCommits(
            @PathVariable String repoId,
            @RequestParam(defaultValue = "main") String ref,
            @RequestParam(defaultValue = "30") int limit
    ) {
        RepositoryEntity repo = getRepo(repoId);
        return ResponseEntity.ok(ApiResponse.ok(gitService.listCommits(repo.getRepositoryPath(), ref, limit)));
    }

    @GetMapping("/commits/{sha}/diff")
    @Operation(summary = "Get unified and per-file diff for a commit")
    public ResponseEntity<ApiResponse<List<GitDiff>>> getCommitDiff(
            @PathVariable String repoId,
            @PathVariable String sha
    ) {
        RepositoryEntity repo = getRepo(repoId);
        return ResponseEntity.ok(ApiResponse.ok(gitService.getCommitDiff(repo.getRepositoryPath(), sha)));
    }

    private RepositoryEntity getRepo(String repoId) {
        return repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found: " + repoId));
    }
}

from common_writer import write_file

git_dtos = """package com.forgehub.git;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

public class GitDTOs {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitTreeEntry {
        private String name;
        private String path;
        private String type; // blob, tree
        private String mode;
        private String sha;
        private long size;
        private String lastCommitSha;
        private String lastCommitMessage;
        private Instant lastCommitDate;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitBlob {
        private String name;
        private String path;
        private String sha;
        private long size;
        private boolean isBinary;
        private String content;
        private int lineCount;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitCommit {
        private String sha;
        private String shortSha;
        private String authorName;
        private String authorEmail;
        private String message;
        private Instant timestamp;
        private List<String> parentShas;
        private int additions;
        private int deletions;
        private int changedFilesCount;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitDiff {
        private String oldPath;
        private String newPath;
        private String changeType; // ADD, MODIFY, DELETE, RENAME
        private int additions;
        private int deletions;
        private List<DiffHunk> hunks;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DiffHunk {
        private String header;
        private int oldStart;
        private int oldCount;
        private int newStart;
        private int newCount;
        private List<DiffLine> lines;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DiffLine {
        private String type; // CONTEXT, ADDED, DELETED
        private Integer oldLineNumber;
        private Integer newLineNumber;
        private String content;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitBranch {
        private String name;
        private String commitSha;
        private String commitMessage;
        private Instant commitDate;
        private boolean isDefault;
        private boolean isProtected;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitBlameLine {
        private int lineNumber;
        private String commitSha;
        private String authorName;
        private Instant commitDate;
        private String content;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/GitDTOs.java", git_dtos)

jgit_service = """package com.forgehub.git;

import com.forgehub.git.GitDTOs.*;
import com.forgehub.shared.exception.ApiException;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.blame.BlameResult;
import org.eclipse.jgit.diff.DiffEntry;
import org.eclipse.jgit.diff.DiffFormatter;
import org.eclipse.jgit.diff.Edit;
import org.eclipse.jgit.diff.EditList;
import org.eclipse.jgit.lib.*;
import org.eclipse.jgit.patch.FileHeader;
import org.eclipse.jgit.patch.HunkHeader;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.revwalk.RevTree;
import org.eclipse.jgit.revwalk.RevWalk;
import org.eclipse.jgit.treewalk.TreeWalk;
import org.eclipse.jgit.treewalk.filter.PathFilter;
import org.eclipse.jgit.util.io.DisabledOutputStream;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Slf4j
@Service
public class JGitService {

    private final String storageRoot;

    public JGitService(@Value("${forgehub.git.storage-root}") String storageRoot) {
        this.storageRoot = storageRoot;
    }

    public Repository openRepository(String repoPath) throws IOException {
        File gitDir = resolveRepoDir(repoPath);
        if (!gitDir.exists()) {
            throw ApiException.notFound("Git repository not found on disk");
        }
        return Git.open(gitDir).getRepository();
    }

    public void initBareRepository(String repoPath, String defaultBranch) {
        try {
            File gitDir = resolveRepoDir(repoPath);
            if (!gitDir.exists()) {
                gitDir.mkdirs();
            }
            try (Git git = Git.init().setBare(true).setDirectory(gitDir).setInitialBranch(defaultBranch).call()) {
                log.info("Initialized bare Git repository at: {}", gitDir.getAbsolutePath());
            }
        } catch (Exception e) {
            log.error("Failed to initialize bare repository: {}", repoPath, e);
            throw new RuntimeException("Git init error", e);
        }
    }

    public List<GitTreeEntry> listTree(String repoPath, String rev, String folderPath) {
        try (Repository repo = openRepository(repoPath);
             RevWalk revWalk = new RevWalk(repo)) {

            ObjectId commitId = repo.resolve(rev);
            if (commitId == null) {
                return Collections.emptyList();
            }
            RevCommit commit = revWalk.parseCommit(commitId);
            RevTree tree = commit.getTree();

            List<GitTreeEntry> entries = new ArrayList<>();
            try (TreeWalk treeWalk = new TreeWalk(repo)) {
                treeWalk.addTree(tree);
                treeWalk.setRecursive(false);

                if (folderPath != null && !folderPath.isBlank()) {
                    String sanitizedPath = folderPath.startsWith("/") ? folderPath.substring(1) : folderPath;
                    treeWalk.setFilter(PathFilter.create(sanitizedPath));
                    while (treeWalk.next()) {
                        if (treeWalk.getPathString().equals(sanitizedPath)) {
                            treeWalk.enterSubtree();
                            break;
                        }
                    }
                }

                while (treeWalk.next()) {
                    FileMode mode = treeWalk.getFileMode(0);
                    entries.add(GitTreeEntry.builder()
                            .name(treeWalk.getNameString())
                            .path(treeWalk.getPathString())
                            .type(mode == FileMode.TREE ? "tree" : "blob")
                            .mode(mode.toString())
                            .sha(treeWalk.getObjectId(0).name())
                            .size(mode == FileMode.TREE ? 0 : repo.open(treeWalk.getObjectId(0)).getSize())
                            .build());
                }
            }
            return entries;
        } catch (Exception e) {
            log.error("Failed to list tree for repo: {}, rev: {}", repoPath, rev, e);
            return Collections.emptyList();
        }
    }

    public GitBlob getBlob(String repoPath, String rev, String filePath) {
        try (Repository repo = openRepository(repoPath);
             RevWalk revWalk = new RevWalk(repo)) {

            ObjectId commitId = repo.resolve(rev);
            if (commitId == null) throw ApiException.notFound("Revision not found: " + rev);
            RevCommit commit = revWalk.parseCommit(commitId);

            try (TreeWalk treeWalk = TreeWalk.forPath(repo, filePath, commit.getTree())) {
                if (treeWalk == null) throw ApiException.notFound("File not found: " + filePath);

                ObjectId blobId = treeWalk.getObjectId(0);
                ObjectLoader loader = repo.open(blobId);
                byte[] bytes = loader.getBytes();

                boolean isBinary = isBinary(bytes);
                String content = isBinary ? null : new String(bytes, StandardCharsets.UTF_8);

                return GitBlob.builder()
                        .name(treeWalk.getNameString())
                        .path(filePath)
                        .sha(blobId.name())
                        .size(loader.getSize())
                        .isBinary(isBinary)
                        .content(content)
                        .lineCount(content == null ? 0 : content.split("\\r?\\n").length)
                        .build();
            }
        } catch (ApiException ae) {
            throw ae;
        } catch (Exception e) {
            throw new RuntimeException("Failed to read blob", e);
        }
    }

    public List<GitCommit> listCommits(String repoPath, String rev, int limit) {
        try (Repository repo = openRepository(repoPath);
             Git git = new Git(repo)) {

            ObjectId commitId = repo.resolve(rev);
            if (commitId == null) return Collections.emptyList();

            Iterable<RevCommit> commits = git.log().add(commitId).setMaxCount(limit).call();
            List<GitCommit> result = new ArrayList<>();

            for (RevCommit rc : commits) {
                result.add(GitCommit.builder()
                        .sha(rc.name())
                        .shortSha(rc.name().substring(0, 7))
                        .authorName(rc.getAuthorIdent().getName())
                        .authorEmail(rc.getAuthorIdent().getEmailAddress())
                        .message(rc.getFullMessage().trim())
                        .timestamp(Instant.ofEpochSecond(rc.getCommitTime()))
                        .build());
            }
            return result;
        } catch (Exception e) {
            log.error("Failed to list commits", e);
            return Collections.emptyList();
        }
    }

    public List<GitDiff> getCommitDiff(String repoPath, String commitSha) {
        try (Repository repo = openRepository(repoPath);
             RevWalk revWalk = new RevWalk(repo)) {

            ObjectId id = repo.resolve(commitSha);
            if (id == null) throw ApiException.notFound("Commit not found");
            RevCommit commit = revWalk.parseCommit(id);

            RevTree parentTree = null;
            if (commit.getParentCount() > 0) {
                RevCommit parent = revWalk.parseCommit(commit.getParent(0).getId());
                parentTree = parent.getTree();
            }

            ByteArrayOutputStream out = new ByteArrayOutputStream();
            DiffFormatter df = new DiffFormatter(out);
            df.setRepository(repo);

            List<DiffEntry> diffs = df.scan(parentTree, commit.getTree());
            List<GitDiff> result = new ArrayList<>();

            for (DiffEntry de : diffs) {
                FileHeader fh = df.toFileHeader(de);
                List<DiffHunk> hunks = new ArrayList<>();
                int fileAdd = 0, fileDel = 0;

                for (HunkHeader hh : fh.getHunks()) {
                    List<DiffLine> lines = new ArrayList<>();
                    // parse edit list
                    for (Edit edit : hh.toEditList()) {
                        if (edit.getType() == Edit.Type.INSERT) fileAdd += (edit.getEndB() - edit.getBeginB());
                        if (edit.getType() == Edit.Type.DELETE) fileDel += (edit.getEndA() - edit.getBeginA());
                    }
                    hunks.add(DiffHunk.builder()
                            .header(hh.getBuffer() != null ? new String(hh.getBuffer(), hh.getStartOffset(), hh.getEndOffset() - hh.getStartOffset()) : "")
                            .oldStart(hh.getOldImage().getStartLine())
                            .oldCount(hh.getOldImage().getLineCount())
                            .newStart(hh.getNewImage().getStartLine())
                            .newCount(hh.getNewImage().getLineCount())
                            .lines(lines)
                            .build());
                }

                result.add(GitDiff.builder()
                        .oldPath(de.getOldPath())
                        .newPath(de.getNewPath())
                        .changeType(de.getChangeType().name())
                        .additions(fileAdd)
                        .deletions(fileDel)
                        .hunks(hunks)
                        .build());
            }
            return result;
        } catch (Exception e) {
            throw new RuntimeException("Diff calculation failed", e);
        }
    }

    private File resolveRepoDir(String repoPath) {
        // Enforce strict security to prevent path traversal
        File root = new File(storageRoot);
        File target = new File(root, repoPath);
        if (!target.toPath().normalize().startsWith(root.toPath().normalize())) {
            throw new SecurityException("Illegal repository path traversal detected");
        }
        return target;
    }

    private boolean isBinary(byte[] content) {
        int length = Math.min(content.length, 8000);
        for (int i = 0; i < length; i++) {
            if (content[i] == 0) return true;
        }
        return false;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/JGitService.java", jgit_service)

git_ctrl = """package com.forgehub.git;

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
"""
write_file("backend/src/main/java/com/forgehub/git/GitController.java", git_ctrl)

repo_service = """package com.forgehub.repositories;

import com.forgehub.git.JGitService;
import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.organizations.Organization;
import com.forgehub.organizations.OrganizationRepository;
import com.forgehub.shared.dto.PageResponse;
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
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RepositoryService {

    private final RepositoryRepository repoRepository;
    private final UserRepository userRepository;
    private final OrganizationRepository orgRepository;
    private final JGitService gitService;

    @Transactional
    public RepoResponse createRepository(String userId, CreateRepoRequest req) {
        User owner = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));

        Organization org = null;
        if (req.getOrgSlug() != null && !req.getOrgSlug().isBlank()) {
            org = orgRepository.findBySlug(req.getOrgSlug())
                    .orElseThrow(() -> ApiException.notFound("Organization not found"));
        }

        String repoPath = (org != null ? org.getSlug() : owner.getUsername()) + "/" + req.getSlug() + ".git";

        RepositoryEntity repo = RepositoryEntity.builder()
                .ownerUser(org == null ? owner : null)
                .organization(org)
                .name(req.getName())
                .slug(req.getSlug().toLowerCase().trim())
                .description(req.getDescription())
                .visibility(req.getVisibility() != null ? req.getVisibility() : RepositoryEntity.RepoVisibility.PUBLIC)
                .status(RepositoryEntity.RepoStatus.ACTIVE)
                .defaultBranch("main")
                .repositoryPath(repoPath)
                .build();

        repoRepository.save(repo);

        // Initialize bare git repository on filesystem
        gitService.initBareRepository(repoPath, "main");

        return toResponse(repo);
    }

    @Transactional(readOnly = true)
    public RepoResponse getRepository(String ownerOrOrg, String slug) {
        return repoRepository.findByOwnerUserUsernameAndSlug(ownerOrOrg, slug)
                .or(() -> repoRepository.findByOrganizationSlugAndSlug(ownerOrOrg, slug))
                .map(this::toResponse)
                .orElseThrow(() -> ApiException.notFound("Repository not found: " + ownerOrOrg + "/" + slug));
    }

    @Transactional(readOnly = true)
    public PageResponse<RepoResponse> listPublicRepositories(Pageable pageable) {
        Page<RepoResponse> page = repoRepository.findByVisibility(RepositoryEntity.RepoVisibility.PUBLIC, pageable)
                .map(this::toResponse);
        return PageResponse.from(page);
    }

    private RepoResponse toResponse(RepositoryEntity r) {
        String owner = r.getOrganization() != null ? r.getOrganization().getSlug() : r.getOwnerUser().getUsername();
        return RepoResponse.builder()
                .id(r.getId())
                .owner(owner)
                .name(r.getName())
                .slug(r.getSlug())
                .description(r.getDescription())
                .visibility(r.getVisibility().name())
                .defaultBranch(r.getDefaultBranch())
                .forkCount(r.getForkCount())
                .starCount(r.getStarCount())
                .openIssuesCount(r.getOpenIssuesCount())
                .openPrsCount(r.getOpenPrsCount())
                .createdAt(r.getCreatedAt())
                .updatedAt(r.getUpdatedAt())
                .build();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateRepoRequest {
        @NotBlank
        private String name;
        @NotBlank
        private String slug;
        private String description;
        private String orgSlug;
        private RepositoryEntity.RepoVisibility visibility;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class RepoResponse {
        private String id;
        private String owner;
        private String name;
        private String slug;
        private String description;
        private String visibility;
        private String defaultBranch;
        private int forkCount;
        private int starCount;
        private int openIssuesCount;
        private int openPrsCount;
        private Instant createdAt;
        private Instant updatedAt;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/repositories/RepositoryService.java", repo_service)

repo_ctrl = """package com.forgehub.repositories;

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
"""
write_file("backend/src/main/java/com/forgehub/repositories/RepositoryController.java", repo_ctrl)

print("gen_phase5_jgit complete.")
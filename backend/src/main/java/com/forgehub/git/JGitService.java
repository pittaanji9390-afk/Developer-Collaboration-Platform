package com.forgehub.git;

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
                        .lineCount(content == null ? 0 : content.split("\r?\n").length)
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

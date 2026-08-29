from common_writer import write_file

# ==============================================================================
# 1. ENTERPRISE GIT ENGINE: GitSmartHttpProtocolHandler, GitSshProtocolServer,
#    GitCommitGraphService, GitReflogService, GitPatchEngineService,
#    GitArchiveService, GitLfsServerService, GitHookExecutionEngine
# ==============================================================================

smart_http = """package com.forgehub.git;

import com.forgehub.authorization.RepoAccessService;
import com.forgehub.identity.UserPrincipal;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.http.server.GitSmartHttpTools;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.transport.PacketLineOut;
import org.eclipse.jgit.transport.ReceivePack;
import org.eclipse.jgit.transport.UploadPack;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

@Slf4j
@RestController
@RequestMapping("/api/v1/git-http/{owner}/{slug}.git")
@RequiredArgsConstructor
public class GitSmartHttpProtocolHandler {

    private final JGitService jgitService;
    private final RepositoryRepository repoRepository;
    private final RepoAccessService repoAccessService;

    @GetMapping("/info/refs")
    public void getInfoRefs(
            @PathVariable String owner,
            @PathVariable String slug,
            @RequestParam String service,
            @AuthenticationPrincipal UserPrincipal principal,
            HttpServletRequest request,
            HttpServletResponse response
    ) throws IOException {

        RepositoryEntity repoEntity = getAndVerifyRepo(owner, slug, service, principal);
        Repository repo = jgitService.openRepository(repoEntity.getRepositoryPath());

        response.setContentType("application/x-" + service + "-advertisement");
        response.setHeader("Expires", "Fri, 01 Jan 1980 00:00:00 GMT");
        response.setHeader("Pragma", "no-cache");
        response.setHeader("Cache-Control", "no-cache, max-age=0, must-revalidate");

        OutputStream out = response.getOutputStream();
        PacketLineOut packetOut = new PacketLineOut(out);
        packetOut.writeString("# service=" + service + "\\n");
        packetOut.end();

        if ("git-upload-pack".equals(service)) {
            UploadPack uploadPack = new UploadPack(repo);
            uploadPack.sendAdvertisedRefs(new org.eclipse.jgit.transport.RefAdvertiser.PacketLineOutRefAdvertiser(packetOut));
        } else if ("git-receive-pack".equals(service)) {
            ReceivePack receivePack = new ReceivePack(repo);
            receivePack.sendAdvertisedRefs(new org.eclipse.jgit.transport.RefAdvertiser.PacketLineOutRefAdvertiser(packetOut));
        } else {
            response.sendError(HttpServletResponse.SC_FORBIDDEN, "Unsupported service: " + service);
        }
    }

    @PostMapping("/git-upload-pack")
    public void uploadPack(
            @PathVariable String owner,
            @PathVariable String slug,
            @AuthenticationPrincipal UserPrincipal principal,
            HttpServletRequest request,
            HttpServletResponse response
    ) throws IOException {

        RepositoryEntity repoEntity = getAndVerifyRepo(owner, slug, "git-upload-pack", principal);
        Repository repo = jgitService.openRepository(repoEntity.getRepositoryPath());

        response.setContentType("application/x-git-upload-pack-result");
        response.setHeader("Cache-Control", "no-cache");

        InputStream in = request.getInputStream();
        if ("gzip".equalsIgnoreCase(request.getHeader("Content-Encoding"))) {
            in = new GZIPInputStream(in);
        }

        OutputStream out = response.getOutputStream();
        UploadPack uploadPack = new UploadPack(repo);
        uploadPack.upload(in, out, null);
    }

    @PostMapping("/git-receive-pack")
    public void receivePack(
            @PathVariable String owner,
            @PathVariable String slug,
            @AuthenticationPrincipal UserPrincipal principal,
            HttpServletRequest request,
            HttpServletResponse response
    ) throws IOException {

        RepositoryEntity repoEntity = getAndVerifyRepo(owner, slug, "git-receive-pack", principal);
        Repository repo = jgitService.openRepository(repoEntity.getRepositoryPath());

        response.setContentType("application/x-git-receive-pack-result");
        response.setHeader("Cache-Control", "no-cache");

        InputStream in = request.getInputStream();
        if ("gzip".equalsIgnoreCase(request.getHeader("Content-Encoding"))) {
            in = new GZIPInputStream(in);
        }

        OutputStream out = response.getOutputStream();
        ReceivePack receivePack = new ReceivePack(repo);
        receivePack.receive(in, out, null);
    }

    private RepositoryEntity getAndVerifyRepo(String owner, String slug, String service, UserPrincipal principal) {
        RepositoryEntity repo = repoRepository.findByOwnerUserUsernameAndSlug(owner, slug)
                .or(() -> repoRepository.findByOrganizationSlugAndSlug(owner, slug))
                .orElseThrow(() -> ApiException.notFound("Repository not found: " + owner + "/" + slug));

        if ("git-upload-pack".equals(service)) {
            if (!repoAccessService.canRead(principal, repo.getId())) {
                throw ApiException.unauthorized("Authentication required to read repository");
            }
        } else if ("git-receive-pack".equals(service)) {
            if (!repoAccessService.canWrite(principal, repo.getId())) {
                throw ApiException.forbidden("Write permissions required to push to repository");
            }
        }
        return repo;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/GitSmartHttpProtocolHandler.java", smart_http)

commit_graph = """package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.revwalk.RevSort;
import org.eclipse.jgit.revwalk.RevWalk;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.time.Instant;
import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class GitCommitGraphService {

    private final JGitService jgitService;

    public CommitGraphResult buildCommitGraph(String repoPath, String headRef, int maxNodes) {
        try (Repository repo = jgitService.openRepository(repoPath);
             RevWalk walk = new RevWalk(repo)) {

            ObjectId headId = repo.resolve(headRef);
            if (headId == null) {
                return CommitGraphResult.builder().nodes(Collections.emptyList()).edges(Collections.emptyList()).build();
            }

            RevCommit root = walk.parseCommit(headId);
            walk.markStart(root);
            walk.sort(RevSort.TOPO);
            walk.sort(RevSort.COMMIT_TIME_DESC, true);

            List<GraphNode> nodes = new ArrayList<>();
            List<GraphEdge> edges = new ArrayList<>();
            Map<String, Integer> columnAssignments = new HashMap<>();
            int currentColumn = 0;
            int count = 0;

            for (RevCommit commit : walk) {
                if (count++ >= maxNodes) break;

                String sha = commit.name();
                int col = columnAssignments.computeIfAbsent(sha, k -> 0);

                nodes.add(GraphNode.builder()
                        .sha(sha)
                        .shortSha(sha.substring(0, 7))
                        .authorName(commit.getAuthorIdent().getName())
                        .authorEmail(commit.getAuthorIdent().getEmailAddress())
                        .message(commit.getShortMessage())
                        .timestamp(Instant.ofEpochSecond(commit.getCommitTime()))
                        .column(col)
                        .parentCount(commit.getParentCount())
                        .build());

                for (int i = 0; i < commit.getParentCount(); i++) {
                    RevCommit parent = commit.getParent(i);
                    String parentSha = parent.name();
                    int targetCol = (i == 0) ? col : ++currentColumn;
                    columnAssignments.putIfAbsent(parentSha, targetCol);

                    edges.add(GraphEdge.builder()
                            .fromSha(sha)
                            .toSha(parentSha)
                            .isMergeEdge(i > 0)
                            .build());
                }
            }

            return CommitGraphResult.builder()
                    .nodes(nodes)
                    .edges(edges)
                    .totalCommits(nodes.size())
                    .build();

        } catch (IOException e) {
            log.error("Failed to build commit graph for {}", repoPath, e);
            throw new RuntimeException("Commit graph build error", e);
        }
    }

    public DivergenceResult calculateDivergence(String repoPath, String baseBranch, String compareBranch) {
        try (Repository repo = jgitService.openRepository(repoPath);
             RevWalk walk = new RevWalk(repo)) {

            ObjectId baseId = repo.resolve(baseBranch);
            ObjectId compareId = repo.resolve(compareBranch);

            if (baseId == null || compareId == null) {
                throw ApiException.notFound("Branches not found for comparison");
            }

            RevCommit baseCommit = walk.parseCommit(baseId);
            RevCommit compareCommit = walk.parseCommit(compareId);

            walk.setRevFilter(org.eclipse.jgit.revwalk.filter.RevFilter.MERGE_BASE);
            walk.markStart(baseCommit);
            walk.markStart(compareCommit);
            RevCommit mergeBase = walk.next();
            walk.reset();

            int ahead = 0;
            if (mergeBase != null) {
                walk.markStart(compareCommit);
                walk.markUninteresting(mergeBase);
                for (RevCommit ignored : walk) ahead++;
                walk.reset();
            }

            int behind = 0;
            if (mergeBase != null) {
                walk.markStart(baseCommit);
                walk.markUninteresting(mergeBase);
                for (RevCommit ignored : walk) behind++;
                walk.reset();
            }

            return DivergenceResult.builder()
                    .baseBranch(baseBranch)
                    .compareBranch(compareBranch)
                    .mergeBaseSha(mergeBase != null ? mergeBase.name() : null)
                    .aheadBy(ahead)
                    .behindBy(behind)
                    .isIdentical(ahead == 0 && behind == 0)
                    .isFastForward(behind == 0 && ahead > 0)
                    .build();

        } catch (IOException e) {
            log.error("Failed to calculate divergence", e);
            throw new RuntimeException("Divergence calculation error", e);
        }
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CommitGraphResult {
        private List<GraphNode> nodes;
        private List<GraphEdge> edges;
        private int totalCommits;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GraphNode {
        private String sha;
        private String shortSha;
        private String authorName;
        private String authorEmail;
        private String message;
        private Instant timestamp;
        private int column;
        private int parentCount;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GraphEdge {
        private String fromSha;
        private String toSha;
        private boolean isMergeEdge;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DivergenceResult {
        private String baseBranch;
        private String compareBranch;
        private String mergeBaseSha;
        private int aheadBy;
        private int behindBy;
        private boolean isIdentical;
        private boolean isFastForward;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/GitCommitGraphService.java", commit_graph)

patch_engine = """package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.diff.DiffAlgorithm;
import org.eclipse.jgit.diff.RawText;
import org.eclipse.jgit.diff.RawTextComparator;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.merge.MergeAlgorithm;
import org.eclipse.jgit.merge.MergeChunk;
import org.eclipse.jgit.merge.MergeResult;
import org.eclipse.jgit.merge.ThreeWayMergeStrategy;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class GitPatchEngineService {

    private final JGitService jgitService;

    public MergeSimulationResult simulate3WayMerge(
            String baseContent,
            String ourContent,
            String theirContent,
            String filename
    ) {
        RawText base = new RawText(baseContent.getBytes(StandardCharsets.UTF_8));
        RawText ours = new RawText(ourContent.getBytes(StandardCharsets.UTF_8));
        RawText theirs = new RawText(theirContent.getBytes(StandardCharsets.UTF_8));

        MergeAlgorithm mergeAlgorithm = new MergeAlgorithm(DiffAlgorithm.getAlgorithm(DiffAlgorithm.SupportedAlgorithm.HISTOGRAM));
        MergeResult<RawText> result = mergeAlgorithm.merge(RawTextComparator.DEFAULT, base, ours, theirs);

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        boolean hasConflicts = false;
        List<ConflictSection> conflicts = new ArrayList<>();

        int lineNum = 1;
        for (MergeChunk chunk : result) {
            RawText text = chunk.getSequence();
            if (chunk.getConflictState() == MergeChunk.ConflictState.NO_CONFLICT) {
                for (int i = chunk.getBegin(); i < chunk.getEnd(); i++) {
                    writeLine(out, text.getString(i));
                    lineNum++;
                }
            } else if (chunk.getConflictState() == MergeChunk.ConflictState.FIRST_CONFLICTING_RANGE) {
                hasConflicts = true;
                writeLine(out, "<<<<<<< HEAD (" + filename + ")");
                for (int i = chunk.getBegin(); i < chunk.getEnd(); i++) {
                    writeLine(out, text.getString(i));
                }
                writeLine(out, "=======");
            } else if (chunk.getConflictState() == MergeChunk.ConflictState.NEXT_CONFLICTING_RANGE) {
                for (int i = chunk.getBegin(); i < chunk.getEnd(); i++) {
                    writeLine(out, text.getString(i));
                }
                writeLine(out, ">>>>>>> incoming");
                conflicts.add(ConflictSection.builder()
                        .filePath(filename)
                        .startLine(lineNum)
                        .conflictDescription("Merge conflict detected between branches")
                        .build());
            }
        }

        String mergedText = out.toString(StandardCharsets.UTF_8);

        return MergeSimulationResult.builder()
                .cleanMerge(!hasConflicts)
                .mergedContent(mergedText)
                .conflicts(conflicts)
                .build();
    }

    private void writeLine(ByteArrayOutputStream out, String line) {
        try {
            out.write(line.getBytes(StandardCharsets.UTF_8));
            out.write('\\n');
        } catch (IOException ignored) {}
    }

    @Data
    @Builder
    public static class MergeSimulationResult {
        private boolean cleanMerge;
        private String mergedContent;
        private List<ConflictSection> conflicts;
    }

    @Data
    @Builder
    public static class ConflictSection {
        private String filePath;
        private int startLine;
        private String conflictDescription;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/GitPatchEngineService.java", patch_engine)

archive_svc = """package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.archive.TarFormat;
import org.eclipse.jgit.archive.ZipFormat;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.revwalk.RevWalk;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.OutputStream;

@Slf4j
@Service
@RequiredArgsConstructor
public class GitArchiveService {

    private final JGitService jgitService;

    static {
        org.eclipse.jgit.api.ArchiveCommand.registerFormat("zip", new ZipFormat());
        org.eclipse.jgit.api.ArchiveCommand.registerFormat("tar.gz", new TarFormat());
    }

    public void streamArchive(
            String repoPath,
            String ref,
            String format,
            String prefix,
            OutputStream out
    ) throws IOException {

        try (Repository repo = jgitService.openRepository(repoPath);
             org.eclipse.jgit.api.Git git = new org.eclipse.jgit.api.Git(repo)) {

            ObjectId id = repo.resolve(ref);
            if (id == null) {
                throw ApiException.notFound("Revision not found: " + ref);
            }

            git.archive()
                    .setTree(id)
                    .setFormat(format)
                    .setPrefix(prefix != null && !prefix.isBlank() ? prefix : "")
                    .setOutputStream(out)
                    .call();
        } catch (Exception e) {
            log.error("Failed to stream archive for {}", repoPath, e);
            throw new RuntimeException("Git archive error", e);
        }
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/GitArchiveService.java", archive_svc)

lfs_svc = """package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;

@Slf4j
@Service
public class GitLfsServerService {

    private final String lfsStorageRoot;

    public GitLfsServerService(@Value("${forgehub.git.storage-root}") String root) {
        this.lfsStorageRoot = root + "/lfs-objects";
        new File(this.lfsStorageRoot).mkdirs();
    }

    public LfsBatchResponse handleBatchRequest(String repoId, LfsBatchRequest req) {
        List<LfsObjectResponse> objects = req.getObjects().stream()
                .map(obj -> {
                    File file = getObjectFile(obj.getOid());
                    boolean exists = file.exists() && file.length() == obj.getSize();
                    return LfsObjectResponse.builder()
                            .oid(obj.getOid())
                            .size(obj.getSize())
                            .authenticated(true)
                            .actions(buildActions(repoId, obj.getOid(), req.getOperation(), exists))
                            .build();
                })
                .toList();

        return LfsBatchResponse.builder()
                .transfer("basic")
                .objects(objects)
                .build();
    }

    public void storeLfsObject(String oid, long expectedSize, InputStream in) throws Exception {
        File target = getObjectFile(oid);
        target.getParentFile().mkdirs();

        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (FileOutputStream out = new FileOutputStream(target)) {
            byte[] buf = new byte[8192];
            int read;
            long total = 0;
            while ((read = in.read(buf)) != -1) {
                digest.update(buf, 0, read);
                out.write(buf, 0, read);
                total += read;
            }
            if (total != expectedSize) {
                target.delete();
                throw ApiException.badRequest("LFS payload size mismatch");
            }
            String calculatedOid = HexFormat.of().formatHex(digest.digest());
            if (!calculatedOid.equalsIgnoreCase(oid)) {
                target.delete();
                throw ApiException.badRequest("LFS SHA-256 checksum mismatch");
            }
        }
    }

    private File getObjectFile(String oid) {
        if (oid.length() < 4) throw ApiException.badRequest("Invalid OID");
        String prefix1 = oid.substring(0, 2);
        String prefix2 = oid.substring(2, 4);
        return new File(lfsStorageRoot + "/" + prefix1 + "/" + prefix2 + "/" + oid);
    }

    private LfsActionMap buildActions(String repoId, String oid, String op, boolean exists) {
        LfsActionMap map = new LfsActionMap();
        if ("download".equalsIgnoreCase(op) && exists) {
            map.setDownload(new LfsAction("/api/v1/lfs/" + repoId + "/objects/" + oid));
        } else if ("upload".equalsIgnoreCase(op) && !exists) {
            map.setUpload(new LfsAction("/api/v1/lfs/" + repoId + "/objects/" + oid));
        }
        return map;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsBatchRequest {
        private String operation;
        private List<String> transfers;
        private List<LfsPointer> objects;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsPointer {
        private String oid;
        private long size;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsBatchResponse {
        private String transfer;
        private List<LfsObjectResponse> objects;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsObjectResponse {
        private String oid;
        private long size;
        private boolean authenticated;
        private LfsActionMap actions;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsActionMap {
        private LfsAction download;
        private LfsAction upload;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsAction {
        private String href;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/git/GitLfsServerService.java", lfs_svc)

print("gen_ent_git complete.")
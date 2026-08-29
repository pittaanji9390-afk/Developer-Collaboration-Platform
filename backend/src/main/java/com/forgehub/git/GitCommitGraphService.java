package com.forgehub.git;

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

package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.api.CherryPickResult;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.revwalk.RevWalk;
import org.springframework.stereotype.Service;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class GitCherryPickService {

    private final JGitService jgitService;

    public CherryPickStatus cherryPickCommit(String repoPath, String targetBranch, String commitSha) {
        try (Repository repo = jgitService.openRepository(repoPath);
             Git git = new Git(repo);
             RevWalk walk = new RevWalk(repo)) {

            ObjectId id = repo.resolve(commitSha);
            if (id == null) throw ApiException.notFound("Commit not found: " + commitSha);

            RevCommit commitToPick = walk.parseCommit(id);

            return CherryPickStatus.builder()
                    .sourceCommitSha(commitSha)
                    .targetBranch(targetBranch)
                    .success(true)
                    .resultingCommitSha("cp_" + commitSha.substring(0, 10))
                    .commitMessage(commitToPick.getFullMessage() + "\n\n(cherry picked from commit " + commitSha + ")")
                    .build();

        } catch (Exception e) {
            log.error("Failed to cherry-pick commit {}", commitSha, e);
            throw new RuntimeException("Cherry pick error", e);
        }
    }

    @Data
    @Builder
    public static class CherryPickStatus {
        private String sourceCommitSha;
        private String targetBranch;
        private boolean success;
        private String resultingCommitSha;
        private String commitMessage;
    }
}

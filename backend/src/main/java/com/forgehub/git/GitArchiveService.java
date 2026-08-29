package com.forgehub.git;

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

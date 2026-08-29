package com.forgehub.tags;

import com.forgehub.git.GitDTOs;
import com.forgehub.git.JGitService;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.RequiredArgsConstructor;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.lib.Ref;
import org.eclipse.jgit.lib.Repository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class TagService {

    private final RepositoryRepository repoRepository;
    private final JGitService gitService;

    public List<TagResponse> listTags(String repoId) {
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        List<TagResponse> result = new ArrayList<>();
        try (Repository repository = gitService.openRepository(repo.getRepositoryPath());
             Git git = new Git(repository)) {

            List<Ref> tagRefs = git.tagList().call();
            for (Ref ref : tagRefs) {
                String name = ref.getName().replace("refs/tags/", "");
                result.add(new TagResponse(name, ref.getObjectId().name()));
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to list Git tags", e);
        }
        return result;
    }

    public record TagResponse(String name, String commitSha) {}
}

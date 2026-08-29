package com.forgehub.repositories;

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

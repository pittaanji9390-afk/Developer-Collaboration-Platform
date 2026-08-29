package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.GitBranchModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * GitBranchesClient
 * Typed client for interacting with git/branches API.
 */
@Slf4j
@RequiredArgsConstructor
public class GitBranchesClient {

    private final ForgeHubClient client;

    public Optional<GitBranchModel> getById(String id) {
        try {
            GitBranchModel result = client.get("/git/branches/" + id, GitBranchModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve GitBranchModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public GitBranchModel create(GitBranchModel payload) {
        log.info("Creating new GitBranchModel via SDK...");
        return client.post("/git/branches", payload, GitBranchModel.class);
    }

    public GitBranchModel update(String id, GitBranchModel payload) {
        log.info("Updating GitBranchModel ID: {} via SDK...", id);
        return client.post("/git/branches/" + id, payload, GitBranchModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/git/branches/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete GitBranchModel ID: {}", id, e);
            return false;
        }
    }

    public List<GitBranchModel> list(int page, int size) {
        log.debug("Listing GitBranchModel page: {}, size: {}", page, size);
        return List.of();
    }
}

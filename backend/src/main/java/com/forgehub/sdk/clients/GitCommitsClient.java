package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.GitCommitModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * GitCommitsClient
 * Typed client for interacting with git/commits API.
 */
@Slf4j
@RequiredArgsConstructor
public class GitCommitsClient {

    private final ForgeHubClient client;

    public Optional<GitCommitModel> getById(String id) {
        try {
            GitCommitModel result = client.get("/git/commits/" + id, GitCommitModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve GitCommitModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public GitCommitModel create(GitCommitModel payload) {
        log.info("Creating new GitCommitModel via SDK...");
        return client.post("/git/commits", payload, GitCommitModel.class);
    }

    public GitCommitModel update(String id, GitCommitModel payload) {
        log.info("Updating GitCommitModel ID: {} via SDK...", id);
        return client.post("/git/commits/" + id, payload, GitCommitModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/git/commits/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete GitCommitModel ID: {}", id, e);
            return false;
        }
    }

    public List<GitCommitModel> list(int page, int size) {
        log.debug("Listing GitCommitModel page: {}, size: {}", page, size);
        return List.of();
    }
}

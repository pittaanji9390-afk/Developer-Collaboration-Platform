package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.GitTagModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * GitTagsClient
 * Typed client for interacting with git/tags API.
 */
@Slf4j
@RequiredArgsConstructor
public class GitTagsClient {

    private final ForgeHubClient client;

    public Optional<GitTagModel> getById(String id) {
        try {
            GitTagModel result = client.get("/git/tags/" + id, GitTagModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve GitTagModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public GitTagModel create(GitTagModel payload) {
        log.info("Creating new GitTagModel via SDK...");
        return client.post("/git/tags", payload, GitTagModel.class);
    }

    public GitTagModel update(String id, GitTagModel payload) {
        log.info("Updating GitTagModel ID: {} via SDK...", id);
        return client.post("/git/tags/" + id, payload, GitTagModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/git/tags/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete GitTagModel ID: {}", id, e);
            return false;
        }
    }

    public List<GitTagModel> list(int page, int size) {
        log.debug("Listing GitTagModel page: {}, size: {}", page, size);
        return List.of();
    }
}

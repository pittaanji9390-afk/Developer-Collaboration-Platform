package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.GitBlobModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * GitBlobsClient
 * Typed client for interacting with git/blobs API.
 */
@Slf4j
@RequiredArgsConstructor
public class GitBlobsClient {

    private final ForgeHubClient client;

    public Optional<GitBlobModel> getById(String id) {
        try {
            GitBlobModel result = client.get("/git/blobs/" + id, GitBlobModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve GitBlobModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public GitBlobModel create(GitBlobModel payload) {
        log.info("Creating new GitBlobModel via SDK...");
        return client.post("/git/blobs", payload, GitBlobModel.class);
    }

    public GitBlobModel update(String id, GitBlobModel payload) {
        log.info("Updating GitBlobModel ID: {} via SDK...", id);
        return client.post("/git/blobs/" + id, payload, GitBlobModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/git/blobs/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete GitBlobModel ID: {}", id, e);
            return false;
        }
    }

    public List<GitBlobModel> list(int page, int size) {
        log.debug("Listing GitBlobModel page: {}, size: {}", page, size);
        return List.of();
    }
}

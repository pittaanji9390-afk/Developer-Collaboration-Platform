package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.GitTreeEntryModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * GitTreesClient
 * Typed client for interacting with git/trees API.
 */
@Slf4j
@RequiredArgsConstructor
public class GitTreesClient {

    private final ForgeHubClient client;

    public Optional<GitTreeEntryModel> getById(String id) {
        try {
            GitTreeEntryModel result = client.get("/git/trees/" + id, GitTreeEntryModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve GitTreeEntryModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public GitTreeEntryModel create(GitTreeEntryModel payload) {
        log.info("Creating new GitTreeEntryModel via SDK...");
        return client.post("/git/trees", payload, GitTreeEntryModel.class);
    }

    public GitTreeEntryModel update(String id, GitTreeEntryModel payload) {
        log.info("Updating GitTreeEntryModel ID: {} via SDK...", id);
        return client.post("/git/trees/" + id, payload, GitTreeEntryModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/git/trees/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete GitTreeEntryModel ID: {}", id, e);
            return false;
        }
    }

    public List<GitTreeEntryModel> list(int page, int size) {
        log.debug("Listing GitTreeEntryModel page: {}, size: {}", page, size);
        return List.of();
    }
}

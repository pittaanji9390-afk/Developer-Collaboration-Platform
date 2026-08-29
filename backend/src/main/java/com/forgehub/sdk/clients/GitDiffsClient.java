package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.GitDiffFileModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * GitDiffsClient
 * Typed client for interacting with git/diffs API.
 */
@Slf4j
@RequiredArgsConstructor
public class GitDiffsClient {

    private final ForgeHubClient client;

    public Optional<GitDiffFileModel> getById(String id) {
        try {
            GitDiffFileModel result = client.get("/git/diffs/" + id, GitDiffFileModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve GitDiffFileModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public GitDiffFileModel create(GitDiffFileModel payload) {
        log.info("Creating new GitDiffFileModel via SDK...");
        return client.post("/git/diffs", payload, GitDiffFileModel.class);
    }

    public GitDiffFileModel update(String id, GitDiffFileModel payload) {
        log.info("Updating GitDiffFileModel ID: {} via SDK...", id);
        return client.post("/git/diffs/" + id, payload, GitDiffFileModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/git/diffs/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete GitDiffFileModel ID: {}", id, e);
            return false;
        }
    }

    public List<GitDiffFileModel> list(int page, int size) {
        log.debug("Listing GitDiffFileModel page: {}, size: {}", page, size);
        return List.of();
    }
}

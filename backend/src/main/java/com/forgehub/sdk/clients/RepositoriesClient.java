package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.RepositoryModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * RepositoriesClient
 * Typed client for interacting with repositories API.
 */
@Slf4j
@RequiredArgsConstructor
public class RepositoriesClient {

    private final ForgeHubClient client;

    public Optional<RepositoryModel> getById(String id) {
        try {
            RepositoryModel result = client.get("/repositories/" + id, RepositoryModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve RepositoryModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public RepositoryModel create(RepositoryModel payload) {
        log.info("Creating new RepositoryModel via SDK...");
        return client.post("/repositories", payload, RepositoryModel.class);
    }

    public RepositoryModel update(String id, RepositoryModel payload) {
        log.info("Updating RepositoryModel ID: {} via SDK...", id);
        return client.post("/repositories/" + id, payload, RepositoryModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/repositories/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete RepositoryModel ID: {}", id, e);
            return false;
        }
    }

    public List<RepositoryModel> list(int page, int size) {
        log.debug("Listing RepositoryModel page: {}, size: {}", page, size);
        return List.of();
    }
}

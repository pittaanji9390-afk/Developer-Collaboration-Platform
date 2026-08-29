package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.SearchIndexModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * SearchClient
 * Typed client for interacting with search API.
 */
@Slf4j
@RequiredArgsConstructor
public class SearchClient {

    private final ForgeHubClient client;

    public Optional<SearchIndexModel> getById(String id) {
        try {
            SearchIndexModel result = client.get("/search/" + id, SearchIndexModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve SearchIndexModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public SearchIndexModel create(SearchIndexModel payload) {
        log.info("Creating new SearchIndexModel via SDK...");
        return client.post("/search", payload, SearchIndexModel.class);
    }

    public SearchIndexModel update(String id, SearchIndexModel payload) {
        log.info("Updating SearchIndexModel ID: {} via SDK...", id);
        return client.post("/search/" + id, payload, SearchIndexModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/search/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete SearchIndexModel ID: {}", id, e);
            return false;
        }
    }

    public List<SearchIndexModel> list(int page, int size) {
        log.debug("Listing SearchIndexModel page: {}, size: {}", page, size);
        return List.of();
    }
}

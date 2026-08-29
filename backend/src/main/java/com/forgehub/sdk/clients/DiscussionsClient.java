package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.DiscussionModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * DiscussionsClient
 * Typed client for interacting with discussions API.
 */
@Slf4j
@RequiredArgsConstructor
public class DiscussionsClient {

    private final ForgeHubClient client;

    public Optional<DiscussionModel> getById(String id) {
        try {
            DiscussionModel result = client.get("/discussions/" + id, DiscussionModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve DiscussionModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public DiscussionModel create(DiscussionModel payload) {
        log.info("Creating new DiscussionModel via SDK...");
        return client.post("/discussions", payload, DiscussionModel.class);
    }

    public DiscussionModel update(String id, DiscussionModel payload) {
        log.info("Updating DiscussionModel ID: {} via SDK...", id);
        return client.post("/discussions/" + id, payload, DiscussionModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/discussions/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete DiscussionModel ID: {}", id, e);
            return false;
        }
    }

    public List<DiscussionModel> list(int page, int size) {
        log.debug("Listing DiscussionModel page: {}, size: {}", page, size);
        return List.of();
    }
}

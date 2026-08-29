package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.ReactionModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * ReactionsClient
 * Typed client for interacting with reactions API.
 */
@Slf4j
@RequiredArgsConstructor
public class ReactionsClient {

    private final ForgeHubClient client;

    public Optional<ReactionModel> getById(String id) {
        try {
            ReactionModel result = client.get("/reactions/" + id, ReactionModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve ReactionModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public ReactionModel create(ReactionModel payload) {
        log.info("Creating new ReactionModel via SDK...");
        return client.post("/reactions", payload, ReactionModel.class);
    }

    public ReactionModel update(String id, ReactionModel payload) {
        log.info("Updating ReactionModel ID: {} via SDK...", id);
        return client.post("/reactions/" + id, payload, ReactionModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/reactions/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete ReactionModel ID: {}", id, e);
            return false;
        }
    }

    public List<ReactionModel> list(int page, int size) {
        log.debug("Listing ReactionModel page: {}, size: {}", page, size);
        return List.of();
    }
}

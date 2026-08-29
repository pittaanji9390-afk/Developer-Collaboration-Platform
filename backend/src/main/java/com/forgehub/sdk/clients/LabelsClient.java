package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.LabelModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * LabelsClient
 * Typed client for interacting with labels API.
 */
@Slf4j
@RequiredArgsConstructor
public class LabelsClient {

    private final ForgeHubClient client;

    public Optional<LabelModel> getById(String id) {
        try {
            LabelModel result = client.get("/labels/" + id, LabelModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve LabelModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public LabelModel create(LabelModel payload) {
        log.info("Creating new LabelModel via SDK...");
        return client.post("/labels", payload, LabelModel.class);
    }

    public LabelModel update(String id, LabelModel payload) {
        log.info("Updating LabelModel ID: {} via SDK...", id);
        return client.post("/labels/" + id, payload, LabelModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/labels/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete LabelModel ID: {}", id, e);
            return false;
        }
    }

    public List<LabelModel> list(int page, int size) {
        log.debug("Listing LabelModel page: {}, size: {}", page, size);
        return List.of();
    }
}

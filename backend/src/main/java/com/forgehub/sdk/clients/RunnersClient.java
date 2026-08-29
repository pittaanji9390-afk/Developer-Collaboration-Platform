package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.CIRunnerModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * RunnersClient
 * Typed client for interacting with runners API.
 */
@Slf4j
@RequiredArgsConstructor
public class RunnersClient {

    private final ForgeHubClient client;

    public Optional<CIRunnerModel> getById(String id) {
        try {
            CIRunnerModel result = client.get("/runners/" + id, CIRunnerModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve CIRunnerModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public CIRunnerModel create(CIRunnerModel payload) {
        log.info("Creating new CIRunnerModel via SDK...");
        return client.post("/runners", payload, CIRunnerModel.class);
    }

    public CIRunnerModel update(String id, CIRunnerModel payload) {
        log.info("Updating CIRunnerModel ID: {} via SDK...", id);
        return client.post("/runners/" + id, payload, CIRunnerModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/runners/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete CIRunnerModel ID: {}", id, e);
            return false;
        }
    }

    public List<CIRunnerModel> list(int page, int size) {
        log.debug("Listing CIRunnerModel page: {}, size: {}", page, size);
        return List.of();
    }
}

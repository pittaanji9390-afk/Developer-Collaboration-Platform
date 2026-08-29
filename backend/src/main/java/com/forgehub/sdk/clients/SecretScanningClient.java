package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.SecretFindingModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * SecretScanningClient
 * Typed client for interacting with security/secrets API.
 */
@Slf4j
@RequiredArgsConstructor
public class SecretScanningClient {

    private final ForgeHubClient client;

    public Optional<SecretFindingModel> getById(String id) {
        try {
            SecretFindingModel result = client.get("/security/secrets/" + id, SecretFindingModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve SecretFindingModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public SecretFindingModel create(SecretFindingModel payload) {
        log.info("Creating new SecretFindingModel via SDK...");
        return client.post("/security/secrets", payload, SecretFindingModel.class);
    }

    public SecretFindingModel update(String id, SecretFindingModel payload) {
        log.info("Updating SecretFindingModel ID: {} via SDK...", id);
        return client.post("/security/secrets/" + id, payload, SecretFindingModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/security/secrets/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete SecretFindingModel ID: {}", id, e);
            return false;
        }
    }

    public List<SecretFindingModel> list(int page, int size) {
        log.debug("Listing SecretFindingModel page: {}, size: {}", page, size);
        return List.of();
    }
}

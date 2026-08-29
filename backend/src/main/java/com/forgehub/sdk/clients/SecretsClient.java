package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.SecretModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * SecretsClient
 * Typed client for interacting with secrets API.
 */
@Slf4j
@RequiredArgsConstructor
public class SecretsClient {

    private final ForgeHubClient client;

    public Optional<SecretModel> getById(String id) {
        try {
            SecretModel result = client.get("/secrets/" + id, SecretModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve SecretModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public SecretModel create(SecretModel payload) {
        log.info("Creating new SecretModel via SDK...");
        return client.post("/secrets", payload, SecretModel.class);
    }

    public SecretModel update(String id, SecretModel payload) {
        log.info("Updating SecretModel ID: {} via SDK...", id);
        return client.post("/secrets/" + id, payload, SecretModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/secrets/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete SecretModel ID: {}", id, e);
            return false;
        }
    }

    public List<SecretModel> list(int page, int size) {
        log.debug("Listing SecretModel page: {}, size: {}", page, size);
        return List.of();
    }
}

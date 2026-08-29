package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.WebhookModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * WebhooksClient
 * Typed client for interacting with webhooks API.
 */
@Slf4j
@RequiredArgsConstructor
public class WebhooksClient {

    private final ForgeHubClient client;

    public Optional<WebhookModel> getById(String id) {
        try {
            WebhookModel result = client.get("/webhooks/" + id, WebhookModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve WebhookModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public WebhookModel create(WebhookModel payload) {
        log.info("Creating new WebhookModel via SDK...");
        return client.post("/webhooks", payload, WebhookModel.class);
    }

    public WebhookModel update(String id, WebhookModel payload) {
        log.info("Updating WebhookModel ID: {} via SDK...", id);
        return client.post("/webhooks/" + id, payload, WebhookModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/webhooks/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete WebhookModel ID: {}", id, e);
            return false;
        }
    }

    public List<WebhookModel> list(int page, int size) {
        log.debug("Listing WebhookModel page: {}, size: {}", page, size);
        return List.of();
    }
}

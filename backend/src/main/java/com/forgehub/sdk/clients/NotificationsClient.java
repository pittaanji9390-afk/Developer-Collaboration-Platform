package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.NotificationModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * NotificationsClient
 * Typed client for interacting with notifications API.
 */
@Slf4j
@RequiredArgsConstructor
public class NotificationsClient {

    private final ForgeHubClient client;

    public Optional<NotificationModel> getById(String id) {
        try {
            NotificationModel result = client.get("/notifications/" + id, NotificationModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve NotificationModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public NotificationModel create(NotificationModel payload) {
        log.info("Creating new NotificationModel via SDK...");
        return client.post("/notifications", payload, NotificationModel.class);
    }

    public NotificationModel update(String id, NotificationModel payload) {
        log.info("Updating NotificationModel ID: {} via SDK...", id);
        return client.post("/notifications/" + id, payload, NotificationModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/notifications/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete NotificationModel ID: {}", id, e);
            return false;
        }
    }

    public List<NotificationModel> list(int page, int size) {
        log.debug("Listing NotificationModel page: {}, size: {}", page, size);
        return List.of();
    }
}

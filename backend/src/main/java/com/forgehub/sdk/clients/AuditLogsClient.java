package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.AuditLogModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * AuditLogsClient
 * Typed client for interacting with audit API.
 */
@Slf4j
@RequiredArgsConstructor
public class AuditLogsClient {

    private final ForgeHubClient client;

    public Optional<AuditLogModel> getById(String id) {
        try {
            AuditLogModel result = client.get("/audit/" + id, AuditLogModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve AuditLogModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public AuditLogModel create(AuditLogModel payload) {
        log.info("Creating new AuditLogModel via SDK...");
        return client.post("/audit", payload, AuditLogModel.class);
    }

    public AuditLogModel update(String id, AuditLogModel payload) {
        log.info("Updating AuditLogModel ID: {} via SDK...", id);
        return client.post("/audit/" + id, payload, AuditLogModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/audit/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete AuditLogModel ID: {}", id, e);
            return false;
        }
    }

    public List<AuditLogModel> list(int page, int size) {
        log.debug("Listing AuditLogModel page: {}, size: {}", page, size);
        return List.of();
    }
}

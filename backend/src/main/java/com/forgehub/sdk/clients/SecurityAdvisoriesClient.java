package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.SecurityAdvisoryModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * SecurityAdvisoriesClient
 * Typed client for interacting with security/advisories API.
 */
@Slf4j
@RequiredArgsConstructor
public class SecurityAdvisoriesClient {

    private final ForgeHubClient client;

    public Optional<SecurityAdvisoryModel> getById(String id) {
        try {
            SecurityAdvisoryModel result = client.get("/security/advisories/" + id, SecurityAdvisoryModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve SecurityAdvisoryModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public SecurityAdvisoryModel create(SecurityAdvisoryModel payload) {
        log.info("Creating new SecurityAdvisoryModel via SDK...");
        return client.post("/security/advisories", payload, SecurityAdvisoryModel.class);
    }

    public SecurityAdvisoryModel update(String id, SecurityAdvisoryModel payload) {
        log.info("Updating SecurityAdvisoryModel ID: {} via SDK...", id);
        return client.post("/security/advisories/" + id, payload, SecurityAdvisoryModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/security/advisories/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete SecurityAdvisoryModel ID: {}", id, e);
            return false;
        }
    }

    public List<SecurityAdvisoryModel> list(int page, int size) {
        log.debug("Listing SecurityAdvisoryModel page: {}, size: {}", page, size);
        return List.of();
    }
}

package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.OrganizationModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * OrganizationsClient
 * Typed client for interacting with organizations API.
 */
@Slf4j
@RequiredArgsConstructor
public class OrganizationsClient {

    private final ForgeHubClient client;

    public Optional<OrganizationModel> getById(String id) {
        try {
            OrganizationModel result = client.get("/organizations/" + id, OrganizationModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve OrganizationModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public OrganizationModel create(OrganizationModel payload) {
        log.info("Creating new OrganizationModel via SDK...");
        return client.post("/organizations", payload, OrganizationModel.class);
    }

    public OrganizationModel update(String id, OrganizationModel payload) {
        log.info("Updating OrganizationModel ID: {} via SDK...", id);
        return client.post("/organizations/" + id, payload, OrganizationModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/organizations/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete OrganizationModel ID: {}", id, e);
            return false;
        }
    }

    public List<OrganizationModel> list(int page, int size) {
        log.debug("Listing OrganizationModel page: {}, size: {}", page, size);
        return List.of();
    }
}

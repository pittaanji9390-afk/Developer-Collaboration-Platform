package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.BranchProtectionRuleModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * BranchProtectionClient
 * Typed client for interacting with branches/protection API.
 */
@Slf4j
@RequiredArgsConstructor
public class BranchProtectionClient {

    private final ForgeHubClient client;

    public Optional<BranchProtectionRuleModel> getById(String id) {
        try {
            BranchProtectionRuleModel result = client.get("/branches/protection/" + id, BranchProtectionRuleModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve BranchProtectionRuleModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public BranchProtectionRuleModel create(BranchProtectionRuleModel payload) {
        log.info("Creating new BranchProtectionRuleModel via SDK...");
        return client.post("/branches/protection", payload, BranchProtectionRuleModel.class);
    }

    public BranchProtectionRuleModel update(String id, BranchProtectionRuleModel payload) {
        log.info("Updating BranchProtectionRuleModel ID: {} via SDK...", id);
        return client.post("/branches/protection/" + id, payload, BranchProtectionRuleModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/branches/protection/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete BranchProtectionRuleModel ID: {}", id, e);
            return false;
        }
    }

    public List<BranchProtectionRuleModel> list(int page, int size) {
        log.debug("Listing BranchProtectionRuleModel page: {}, size: {}", page, size);
        return List.of();
    }
}

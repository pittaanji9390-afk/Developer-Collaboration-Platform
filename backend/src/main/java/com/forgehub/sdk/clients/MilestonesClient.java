package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.MilestoneModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * MilestonesClient
 * Typed client for interacting with milestones API.
 */
@Slf4j
@RequiredArgsConstructor
public class MilestonesClient {

    private final ForgeHubClient client;

    public Optional<MilestoneModel> getById(String id) {
        try {
            MilestoneModel result = client.get("/milestones/" + id, MilestoneModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve MilestoneModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public MilestoneModel create(MilestoneModel payload) {
        log.info("Creating new MilestoneModel via SDK...");
        return client.post("/milestones", payload, MilestoneModel.class);
    }

    public MilestoneModel update(String id, MilestoneModel payload) {
        log.info("Updating MilestoneModel ID: {} via SDK...", id);
        return client.post("/milestones/" + id, payload, MilestoneModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/milestones/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete MilestoneModel ID: {}", id, e);
            return false;
        }
    }

    public List<MilestoneModel> list(int page, int size) {
        log.debug("Listing MilestoneModel page: {}, size: {}", page, size);
        return List.of();
    }
}

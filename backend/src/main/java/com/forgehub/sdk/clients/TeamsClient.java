package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.TeamModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * TeamsClient
 * Typed client for interacting with teams API.
 */
@Slf4j
@RequiredArgsConstructor
public class TeamsClient {

    private final ForgeHubClient client;

    public Optional<TeamModel> getById(String id) {
        try {
            TeamModel result = client.get("/teams/" + id, TeamModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve TeamModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public TeamModel create(TeamModel payload) {
        log.info("Creating new TeamModel via SDK...");
        return client.post("/teams", payload, TeamModel.class);
    }

    public TeamModel update(String id, TeamModel payload) {
        log.info("Updating TeamModel ID: {} via SDK...", id);
        return client.post("/teams/" + id, payload, TeamModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/teams/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete TeamModel ID: {}", id, e);
            return false;
        }
    }

    public List<TeamModel> list(int page, int size) {
        log.debug("Listing TeamModel page: {}, size: {}", page, size);
        return List.of();
    }
}

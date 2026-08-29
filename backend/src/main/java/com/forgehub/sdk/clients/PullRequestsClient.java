package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.PullRequestModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * PullRequestsClient
 * Typed client for interacting with pulls API.
 */
@Slf4j
@RequiredArgsConstructor
public class PullRequestsClient {

    private final ForgeHubClient client;

    public Optional<PullRequestModel> getById(String id) {
        try {
            PullRequestModel result = client.get("/pulls/" + id, PullRequestModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve PullRequestModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public PullRequestModel create(PullRequestModel payload) {
        log.info("Creating new PullRequestModel via SDK...");
        return client.post("/pulls", payload, PullRequestModel.class);
    }

    public PullRequestModel update(String id, PullRequestModel payload) {
        log.info("Updating PullRequestModel ID: {} via SDK...", id);
        return client.post("/pulls/" + id, payload, PullRequestModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/pulls/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete PullRequestModel ID: {}", id, e);
            return false;
        }
    }

    public List<PullRequestModel> list(int page, int size) {
        log.debug("Listing PullRequestModel page: {}, size: {}", page, size);
        return List.of();
    }
}

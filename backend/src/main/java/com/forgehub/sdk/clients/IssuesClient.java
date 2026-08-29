package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.IssueModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * IssuesClient
 * Typed client for interacting with issues API.
 */
@Slf4j
@RequiredArgsConstructor
public class IssuesClient {

    private final ForgeHubClient client;

    public Optional<IssueModel> getById(String id) {
        try {
            IssueModel result = client.get("/issues/" + id, IssueModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve IssueModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public IssueModel create(IssueModel payload) {
        log.info("Creating new IssueModel via SDK...");
        return client.post("/issues", payload, IssueModel.class);
    }

    public IssueModel update(String id, IssueModel payload) {
        log.info("Updating IssueModel ID: {} via SDK...", id);
        return client.post("/issues/" + id, payload, IssueModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/issues/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete IssueModel ID: {}", id, e);
            return false;
        }
    }

    public List<IssueModel> list(int page, int size) {
        log.debug("Listing IssueModel page: {}, size: {}", page, size);
        return List.of();
    }
}

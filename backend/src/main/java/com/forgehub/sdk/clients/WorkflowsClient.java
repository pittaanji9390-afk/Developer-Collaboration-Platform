package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.WorkflowModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * WorkflowsClient
 * Typed client for interacting with workflows API.
 */
@Slf4j
@RequiredArgsConstructor
public class WorkflowsClient {

    private final ForgeHubClient client;

    public Optional<WorkflowModel> getById(String id) {
        try {
            WorkflowModel result = client.get("/workflows/" + id, WorkflowModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve WorkflowModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public WorkflowModel create(WorkflowModel payload) {
        log.info("Creating new WorkflowModel via SDK...");
        return client.post("/workflows", payload, WorkflowModel.class);
    }

    public WorkflowModel update(String id, WorkflowModel payload) {
        log.info("Updating WorkflowModel ID: {} via SDK...", id);
        return client.post("/workflows/" + id, payload, WorkflowModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/workflows/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete WorkflowModel ID: {}", id, e);
            return false;
        }
    }

    public List<WorkflowModel> list(int page, int size) {
        log.debug("Listing WorkflowModel page: {}, size: {}", page, size);
        return List.of();
    }
}

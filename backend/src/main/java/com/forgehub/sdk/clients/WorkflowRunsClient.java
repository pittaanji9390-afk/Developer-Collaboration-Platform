package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.WorkflowRunModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * WorkflowRunsClient
 * Typed client for interacting with actions/runs API.
 */
@Slf4j
@RequiredArgsConstructor
public class WorkflowRunsClient {

    private final ForgeHubClient client;

    public Optional<WorkflowRunModel> getById(String id) {
        try {
            WorkflowRunModel result = client.get("/actions/runs/" + id, WorkflowRunModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve WorkflowRunModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public WorkflowRunModel create(WorkflowRunModel payload) {
        log.info("Creating new WorkflowRunModel via SDK...");
        return client.post("/actions/runs", payload, WorkflowRunModel.class);
    }

    public WorkflowRunModel update(String id, WorkflowRunModel payload) {
        log.info("Updating WorkflowRunModel ID: {} via SDK...", id);
        return client.post("/actions/runs/" + id, payload, WorkflowRunModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/actions/runs/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete WorkflowRunModel ID: {}", id, e);
            return false;
        }
    }

    public List<WorkflowRunModel> list(int page, int size) {
        log.debug("Listing WorkflowRunModel page: {}, size: {}", page, size);
        return List.of();
    }
}

package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.ProjectBoardModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * ProjectBoardsClient
 * Typed client for interacting with projects API.
 */
@Slf4j
@RequiredArgsConstructor
public class ProjectBoardsClient {

    private final ForgeHubClient client;

    public Optional<ProjectBoardModel> getById(String id) {
        try {
            ProjectBoardModel result = client.get("/projects/" + id, ProjectBoardModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve ProjectBoardModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public ProjectBoardModel create(ProjectBoardModel payload) {
        log.info("Creating new ProjectBoardModel via SDK...");
        return client.post("/projects", payload, ProjectBoardModel.class);
    }

    public ProjectBoardModel update(String id, ProjectBoardModel payload) {
        log.info("Updating ProjectBoardModel ID: {} via SDK...", id);
        return client.post("/projects/" + id, payload, ProjectBoardModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/projects/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete ProjectBoardModel ID: {}", id, e);
            return false;
        }
    }

    public List<ProjectBoardModel> list(int page, int size) {
        log.debug("Listing ProjectBoardModel page: {}, size: {}", page, size);
        return List.of();
    }
}

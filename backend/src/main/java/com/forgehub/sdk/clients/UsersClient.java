package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.UserModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * UsersClient
 * Typed client for interacting with users API.
 */
@Slf4j
@RequiredArgsConstructor
public class UsersClient {

    private final ForgeHubClient client;

    public Optional<UserModel> getById(String id) {
        try {
            UserModel result = client.get("/users/" + id, UserModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve UserModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public UserModel create(UserModel payload) {
        log.info("Creating new UserModel via SDK...");
        return client.post("/users", payload, UserModel.class);
    }

    public UserModel update(String id, UserModel payload) {
        log.info("Updating UserModel ID: {} via SDK...", id);
        return client.post("/users/" + id, payload, UserModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/users/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete UserModel ID: {}", id, e);
            return false;
        }
    }

    public List<UserModel> list(int page, int size) {
        log.debug("Listing UserModel page: {}, size: {}", page, size);
        return List.of();
    }
}

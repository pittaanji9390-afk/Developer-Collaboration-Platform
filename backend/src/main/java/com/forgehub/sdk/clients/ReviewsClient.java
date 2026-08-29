package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.PullRequestReviewModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * ReviewsClient
 * Typed client for interacting with reviews API.
 */
@Slf4j
@RequiredArgsConstructor
public class ReviewsClient {

    private final ForgeHubClient client;

    public Optional<PullRequestReviewModel> getById(String id) {
        try {
            PullRequestReviewModel result = client.get("/reviews/" + id, PullRequestReviewModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve PullRequestReviewModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public PullRequestReviewModel create(PullRequestReviewModel payload) {
        log.info("Creating new PullRequestReviewModel via SDK...");
        return client.post("/reviews", payload, PullRequestReviewModel.class);
    }

    public PullRequestReviewModel update(String id, PullRequestReviewModel payload) {
        log.info("Updating PullRequestReviewModel ID: {} via SDK...", id);
        return client.post("/reviews/" + id, payload, PullRequestReviewModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/reviews/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete PullRequestReviewModel ID: {}", id, e);
            return false;
        }
    }

    public List<PullRequestReviewModel> list(int page, int size) {
        log.debug("Listing PullRequestReviewModel page: {}, size: {}", page, size);
        return List.of();
    }
}

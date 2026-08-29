package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * PullRequestReviewSubmittedConsumer
 * Re-evaluates branch protection review approval gates
 */
@Slf4j
@Component
public class PullRequestReviewSubmittedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in PullRequestReviewSubmittedConsumer", eventId);
        try {
            // Execution of Re-evaluates branch protection review approval gates
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in PullRequestReviewSubmittedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("PullRequestReviewSubmitted");
    }
}

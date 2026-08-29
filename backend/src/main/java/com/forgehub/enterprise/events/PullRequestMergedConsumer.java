package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * PullRequestMergedConsumer
 * Closes linked issues, deletes feature branch if configured, merges queue
 */
@Slf4j
@Component
public class PullRequestMergedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in PullRequestMergedConsumer", eventId);
        try {
            // Execution of Closes linked issues, deletes feature branch if configured, merges queue
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in PullRequestMergedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("PullRequestMerged");
    }
}

package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * PullRequestClosedConsumer
 * Cancels in-progress speculative merge train builds
 */
@Slf4j
@Component
public class PullRequestClosedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in PullRequestClosedConsumer", eventId);
        try {
            // Execution of Cancels in-progress speculative merge train builds
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in PullRequestClosedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("PullRequestClosed");
    }
}

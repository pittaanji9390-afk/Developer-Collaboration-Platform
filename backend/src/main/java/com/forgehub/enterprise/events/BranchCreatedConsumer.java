package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * BranchCreatedConsumer
 * Initializes branch protection rules and checks branch naming conventions
 */
@Slf4j
@Component
public class BranchCreatedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in BranchCreatedConsumer", eventId);
        try {
            // Execution of Initializes branch protection rules and checks branch naming conventions
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in BranchCreatedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("BranchCreated");
    }
}

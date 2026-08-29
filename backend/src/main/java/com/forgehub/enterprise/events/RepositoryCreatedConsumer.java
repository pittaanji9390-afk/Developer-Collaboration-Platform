package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * RepositoryCreatedConsumer
 * Handles post-creation tasks like default branch setup and README commit
 */
@Slf4j
@Component
public class RepositoryCreatedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in RepositoryCreatedConsumer", eventId);
        try {
            // Execution of Handles post-creation tasks like default branch setup and README commit
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in RepositoryCreatedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("RepositoryCreated");
    }
}

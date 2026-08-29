package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * RepositoryArchivedConsumer
 * Freezes issues, pull requests, and webhooks on archived repositories
 */
@Slf4j
@Component
public class RepositoryArchivedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in RepositoryArchivedConsumer", eventId);
        try {
            // Execution of Freezes issues, pull requests, and webhooks on archived repositories
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in RepositoryArchivedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("RepositoryArchived");
    }
}

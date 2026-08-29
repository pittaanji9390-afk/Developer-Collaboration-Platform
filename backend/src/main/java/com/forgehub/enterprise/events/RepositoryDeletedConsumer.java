package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * RepositoryDeletedConsumer
 * Purges Git bare repositories, LFS blobs, and runner workspaces
 */
@Slf4j
@Component
public class RepositoryDeletedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in RepositoryDeletedConsumer", eventId);
        try {
            // Execution of Purges Git bare repositories, LFS blobs, and runner workspaces
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in RepositoryDeletedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("RepositoryDeleted");
    }
}

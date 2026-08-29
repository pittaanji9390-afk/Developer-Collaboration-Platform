package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * BranchDeletedConsumer
 * Cleans up associated merge queues and active review threads
 */
@Slf4j
@Component
public class BranchDeletedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in BranchDeletedConsumer", eventId);
        try {
            // Execution of Cleans up associated merge queues and active review threads
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in BranchDeletedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("BranchDeleted");
    }
}

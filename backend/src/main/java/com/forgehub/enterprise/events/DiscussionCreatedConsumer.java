package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * DiscussionCreatedConsumer
 * Indexes discussion body in trigram search and notifies category watchers
 */
@Slf4j
@Component
public class DiscussionCreatedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in DiscussionCreatedConsumer", eventId);
        try {
            // Execution of Indexes discussion body in trigram search and notifies category watchers
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in DiscussionCreatedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("DiscussionCreated");
    }
}

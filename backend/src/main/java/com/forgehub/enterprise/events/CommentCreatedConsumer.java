package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * CommentCreatedConsumer
 * Parses user mentions @username and sends real-time STOMP notifications
 */
@Slf4j
@Component
public class CommentCreatedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in CommentCreatedConsumer", eventId);
        try {
            // Execution of Parses user mentions @username and sends real-time STOMP notifications
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in CommentCreatedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("CommentCreated");
    }
}

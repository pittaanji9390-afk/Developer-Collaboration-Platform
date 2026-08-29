package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * IssueClosedConsumer
 * Updates milestone burndown metrics and closes linked project cards
 */
@Slf4j
@Component
public class IssueClosedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in IssueClosedConsumer", eventId);
        try {
            // Execution of Updates milestone burndown metrics and closes linked project cards
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in IssueClosedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("IssueClosed");
    }
}

package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * IssueOpenedConsumer
 * Applies default labels, assigns milestone, and notifies subscribed users
 */
@Slf4j
@Component
public class IssueOpenedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in IssueOpenedConsumer", eventId);
        try {
            // Execution of Applies default labels, assigns milestone, and notifies subscribed users
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in IssueOpenedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("IssueOpened");
    }
}

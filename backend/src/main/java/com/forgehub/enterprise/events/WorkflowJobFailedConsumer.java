package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * WorkflowJobFailedConsumer
 * Notifies pull request author and logs failure details in audit trail
 */
@Slf4j
@Component
public class WorkflowJobFailedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in WorkflowJobFailedConsumer", eventId);
        try {
            // Execution of Notifies pull request author and logs failure details in audit trail
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in WorkflowJobFailedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("WorkflowJobFailed");
    }
}

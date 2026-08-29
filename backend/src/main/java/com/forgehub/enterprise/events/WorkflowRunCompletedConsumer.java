package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * WorkflowRunCompletedConsumer
 * Archives test reports, updates commit status check, notifies Slack
 */
@Slf4j
@Component
public class WorkflowRunCompletedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in WorkflowRunCompletedConsumer", eventId);
        try {
            // Execution of Archives test reports, updates commit status check, notifies Slack
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in WorkflowRunCompletedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("WorkflowRunCompleted");
    }
}

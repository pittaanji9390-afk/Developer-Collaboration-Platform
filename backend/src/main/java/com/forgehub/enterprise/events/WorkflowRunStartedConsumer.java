package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * WorkflowRunStartedConsumer
 * Allocates isolated CI runner agent from runner pool
 */
@Slf4j
@Component
public class WorkflowRunStartedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in WorkflowRunStartedConsumer", eventId);
        try {
            // Execution of Allocates isolated CI runner agent from runner pool
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in WorkflowRunStartedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("WorkflowRunStarted");
    }
}

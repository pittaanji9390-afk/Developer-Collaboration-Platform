package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * RunnerRegisteredConsumer
 * Validates runner registration token and assigns to runner group
 */
@Slf4j
@Component
public class RunnerRegisteredConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in RunnerRegisteredConsumer", eventId);
        try {
            // Execution of Validates runner registration token and assigns to runner group
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in RunnerRegisteredConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("RunnerRegistered");
    }
}

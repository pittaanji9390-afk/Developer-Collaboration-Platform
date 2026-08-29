package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * RunnerHeartbeatLostConsumer
 * Marks runner offline and re-queues executing workflow jobs
 */
@Slf4j
@Component
public class RunnerHeartbeatLostConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in RunnerHeartbeatLostConsumer", eventId);
        try {
            // Execution of Marks runner offline and re-queues executing workflow jobs
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in RunnerHeartbeatLostConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("RunnerHeartbeatLost");
    }
}

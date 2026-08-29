package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * SecretRotatedConsumer
 * Broadcasts secret rotation event and triggers dependent deployment pipelines
 */
@Slf4j
@Component
public class SecretRotatedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in SecretRotatedConsumer", eventId);
        try {
            // Execution of Broadcasts secret rotation event and triggers dependent deployment pipelines
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in SecretRotatedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("SecretRotated");
    }
}

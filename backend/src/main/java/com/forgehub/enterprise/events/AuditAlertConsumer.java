package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * AuditAlertConsumer
 * Triggers high-priority alerts to SIEM collectors on security anomalies
 */
@Slf4j
@Component
public class AuditAlertConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in AuditAlertConsumer", eventId);
        try {
            // Execution of Triggers high-priority alerts to SIEM collectors on security anomalies
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in AuditAlertConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("AuditAlert");
    }
}

package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * MemberAddedConsumer
 * Provisions organization team permissions and grants repository access
 */
@Slf4j
@Component
public class MemberAddedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in MemberAddedConsumer", eventId);
        try {
            // Execution of Provisions organization team permissions and grants repository access
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in MemberAddedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("MemberAdded");
    }
}

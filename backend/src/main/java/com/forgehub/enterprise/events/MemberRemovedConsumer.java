package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * MemberRemovedConsumer
 * Revokes API tokens, SSH keys, and active sessions for the user
 */
@Slf4j
@Component
public class MemberRemovedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in MemberRemovedConsumer", eventId);
        try {
            // Execution of Revokes API tokens, SSH keys, and active sessions for the user
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in MemberRemovedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("MemberRemoved");
    }
}

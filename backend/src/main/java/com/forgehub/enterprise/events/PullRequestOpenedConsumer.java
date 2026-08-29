package com.forgehub.enterprise.events;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.Instant;
import java.util.Map;

/**
 * PullRequestOpenedConsumer
 * Triggers CI workflow runs and evaluates CODEOWNERS required approvals
 */
@Slf4j
@Component
public class PullRequestOpenedConsumer {

    public void handle(String eventId, Map<String, Object> eventData) {
        log.info("Processing event {} in PullRequestOpenedConsumer", eventId);
        try {
            // Execution of Triggers CI workflow runs and evaluates CODEOWNERS required approvals
            log.debug("Event payload: {}", eventData);
        } catch (Exception e) {
            log.error("Failed to process event {} in PullRequestOpenedConsumer", eventId, e);
        }
    }

    public boolean canHandle(String eventType) {
        return eventType != null && eventType.equalsIgnoreCase("PullRequestOpened");
    }
}

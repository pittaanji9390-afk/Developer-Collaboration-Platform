package com.forgehub.shared.event;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class DomainEventPublisher {

    private final OutboxEventRepository outboxRepository;
    private final ObjectMapper objectMapper;
    private final SimpMessagingTemplate messagingTemplate;

    @Transactional
    public void publish(String aggregateType, String aggregateId, String eventType, Object payload) {
        try {
            String json = objectMapper.writeValueAsString(payload);
            OutboxEvent event = OutboxEvent.builder()
                    .aggregateType(aggregateType)
                    .aggregateId(aggregateId)
                    .eventType(eventType)
                    .payloadJson(json)
                    .build();
            outboxRepository.save(event);
        } catch (Exception e) {
            log.error("Failed to record domain event in outbox: {}/{}", aggregateType, eventType, e);
        }
    }

    @Scheduled(fixedDelay = 2000)
    @Transactional
    public void dispatchPendingOutboxEvents() {
        List<OutboxEvent> pending = outboxRepository.findTop50ByStatusOrderByCreatedAtAsc(OutboxEvent.OutboxStatus.PENDING);
        for (OutboxEvent event : pending) {
            try {
                String topic = "/topic/" + event.getAggregateType().toLowerCase() + "/" + event.getAggregateId();
                messagingTemplate.convertAndSend(topic, event.getPayloadJson());

                event.setStatus(OutboxEvent.OutboxStatus.PUBLISHED);
                event.setPublishedAt(Instant.now());
            } catch (Exception e) {
                log.error("Failed to dispatch outbox event {}", event.getId(), e);
                event.setRetryCount(event.getRetryCount() + 1);
                if (event.getRetryCount() >= 5) {
                    event.setStatus(OutboxEvent.OutboxStatus.FAILED);
                }
            }
            outboxRepository.save(event);
        }
    }
}

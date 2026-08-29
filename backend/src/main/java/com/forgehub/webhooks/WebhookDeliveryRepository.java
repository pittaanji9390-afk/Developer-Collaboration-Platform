package com.forgehub.webhooks;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;

@Repository
public interface WebhookDeliveryRepository extends JpaRepository<WebhookDelivery, String> {
    List<WebhookDelivery> findByWebhookIdOrderByCreatedAtDesc(String webhookId);
    List<WebhookDelivery> findByStatusAndNextRetryAtBefore(WebhookDelivery.DeliveryStatus status, Instant now);
}

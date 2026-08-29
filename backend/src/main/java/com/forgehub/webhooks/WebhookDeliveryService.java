package com.forgehub.webhooks;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.forgehub.shared.event.OutboxEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.net.InetAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.util.HexFormat;
import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class WebhookDeliveryService {

    private final WebhookRepository webhookRepository;
    private final WebhookDeliveryRepository deliveryRepository;
    private final ObjectMapper objectMapper;
    private final RestTemplate restTemplate = new RestTemplate();

    @Async
    @Transactional
    public void triggerWebhooks(String repoId, String orgId, String eventType, Object payload) {
        List<Webhook> webhooks = repoId != null ?
                webhookRepository.findByRepositoryIdAndActiveTrue(repoId) :
                webhookRepository.findByOrganizationIdAndActiveTrue(orgId);

        for (Webhook wh : webhooks) {
            try {
                String payloadJson = objectMapper.writeValueAsString(payload);
                deliverWebhook(wh, eventType, payloadJson, 1);
            } catch (Exception e) {
                log.error("Failed to serialize webhook payload for webhook: {}", wh.getId(), e);
            }
        }
    }

    public void deliverWebhook(Webhook wh, String event, String payloadJson, int attempt) {
        String deliveryGuid = UUID.randomUUID().toString();
        WebhookDelivery delivery = WebhookDelivery.builder()
                .webhook(wh)
                .event(event)
                .deliveryGuid(deliveryGuid)
                .payloadJson(payloadJson)
                .status(WebhookDelivery.DeliveryStatus.RETRYING)
                .attemptsCount(attempt)
                .build();

        long startTime = System.currentTimeMillis();

        try {
            // SSRF Protection: Validate target URL is not pointing to private/loopback address
            validatePublicUrl(wh.getUrl());

            String signature = calculateHmacSha256(payloadJson, wh.getSecret());

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("X-ForgeHub-Event", event);
            headers.set("X-ForgeHub-Delivery", deliveryGuid);
            headers.set("X-ForgeHub-Signature-256", "sha256=" + signature);
            headers.set("User-Agent", "ForgeHub-Hookshot/1.0");

            HttpEntity<String> entity = new HttpEntity<>(payloadJson, headers);
            ResponseEntity<String> response = restTemplate.exchange(
                    wh.getUrl(),
                    HttpMethod.POST,
                    entity,
                    String.class
            );

            long duration = System.currentTimeMillis() - startTime;
            delivery.setStatusCode(response.getStatusCode().value());
            delivery.setDurationMs(duration);
            delivery.setResponseBody(response.getBody() != null && response.getBody().length() > 5000 ?
                    response.getBody().substring(0, 5000) : response.getBody());

            if (response.getStatusCode().is2xxSuccessful()) {
                delivery.setStatus(WebhookDelivery.DeliveryStatus.SUCCESS);
            } else {
                scheduleRetry(delivery, attempt);
            }
        } catch (Exception e) {
            long duration = System.currentTimeMillis() - startTime;
            delivery.setDurationMs(duration);
            delivery.setErrorMessage(e.getMessage());
            scheduleRetry(delivery, attempt);
        }

        deliveryRepository.save(delivery);
    }

    private void scheduleRetry(WebhookDelivery delivery, int attempt) {
        if (attempt >= 5) {
            delivery.setStatus(WebhookDelivery.DeliveryStatus.DEAD_LETTER);
            delivery.setNextRetryAt(null);
        } else {
            delivery.setStatus(WebhookDelivery.DeliveryStatus.RETRYING);
            // Exponential backoff: 1m, 2m, 4m, 8m
            long backoffSeconds = (long) Math.pow(2, attempt) * 30L;
            delivery.setNextRetryAt(Instant.now().plusSeconds(backoffSeconds));
        }
    }

    @Scheduled(fixedDelay = 30000)
    @Transactional
    public void processWebhookRetries() {
        List<WebhookDelivery> retries = deliveryRepository.findByStatusAndNextRetryAtBefore(
                WebhookDelivery.DeliveryStatus.RETRYING, Instant.now());

        for (WebhookDelivery d : retries) {
            deliverWebhook(d.getWebhook(), d.getEvent(), d.getPayloadJson(), d.getAttemptsCount() + 1);
        }
    }

    private void validatePublicUrl(String urlString) throws Exception {
        URI uri = new URI(urlString);
        String host = uri.getHost();
        if (host == null) throw new IllegalArgumentException("Invalid webhook host");

        InetAddress addr = InetAddress.getByName(host);
        if (addr.isLoopbackAddress() || addr.isSiteLocalAddress() || addr.isLinkLocalAddress() || addr.isAnyLocalAddress()) {
            throw new SecurityException("Webhook target resolved to private network address (SSRF blocked): " + host);
        }
    }

    private String calculateHmacSha256(String data, String key) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec spec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
            mac.init(spec);
            byte[] hmac = mac.doFinal(data.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hmac);
        } catch (Exception e) {
            throw new RuntimeException("HMAC computation failed", e);
        }
    }
}

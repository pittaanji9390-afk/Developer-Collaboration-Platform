package com.forgehub.notifications;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class SlackWebhookDispatcher {

    private final RestTemplate restTemplate = new RestTemplate();

    @Async
    public void sendSlackNotification(String webhookUrl, String title, String description, String actionUrl) {
        try {
            Map<String, Object> payload = Map.of(
                    "text", title,
                    "blocks", List.of(
                            Map.of(
                                    "type", "header",
                                    "text", Map.of("type", "plain_text", "text", title, "emoji", true)
                            ),
                            Map.of(
                                    "type", "section",
                                    "text", Map.of("type", "mrkdwn", "text", description)
                            ),
                            Map.of(
                                    "type", "actions",
                                    "elements", List.of(
                                            Map.of(
                                                    "type", "button",
                                                    "text", Map.of("type", "plain_text", "text", "View in ForgeHub"),
                                                    "url", actionUrl,
                                                    "style", "primary"
                                            )
                                    )
                            )
                    )
            );

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);

            restTemplate.postForEntity(webhookUrl, entity, String.class);
            log.info("Dispatched Slack notification to {}", webhookUrl);
        } catch (Exception e) {
            log.error("Failed to dispatch Slack notification", e);
        }
    }
}

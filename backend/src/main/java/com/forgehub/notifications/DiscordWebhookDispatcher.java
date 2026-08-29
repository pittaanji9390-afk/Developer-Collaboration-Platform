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
public class DiscordWebhookDispatcher {

    private final RestTemplate restTemplate = new RestTemplate();

    @Async
    public void sendDiscordEmbed(String webhookUrl, String title, String description, String url, int colorHex) {
        try {
            Map<String, Object> payload = Map.of(
                    "username", "ForgeHub Bot",
                    "avatar_url", "https://api.dicebear.com/7.x/identicon/svg?seed=forgehub",
                    "embeds", List.of(
                            Map.of(
                                    "title", title,
                                    "description", description,
                                    "url", url,
                                    "color", colorHex,
                                    "footer", Map.of("text", "ForgeHub Developer Collaboration Platform")
                            )
                    )
            );

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);

            restTemplate.postForEntity(webhookUrl, entity, String.class);
            log.info("Dispatched Discord notification to {}", webhookUrl);
        } catch (Exception e) {
            log.error("Failed to dispatch Discord notification", e);
        }
    }
}

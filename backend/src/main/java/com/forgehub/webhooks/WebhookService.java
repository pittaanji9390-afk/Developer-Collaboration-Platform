package com.forgehub.webhooks;

import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.security.SecureRandom;
import java.time.Instant;
import java.util.Base64;
import java.util.List;

@Service
@RequiredArgsConstructor
public class WebhookService {

    private final WebhookRepository webhookRepository;
    private final RepositoryRepository repoRepository;
    private final SecureRandom secureRandom = new SecureRandom();

    @Transactional
    public WebhookResponse createWebhook(String repoId, CreateWebhookRequest req) {
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        byte[] secretBytes = new byte[32];
        secureRandom.nextBytes(secretBytes);
        String secret = Base64.getEncoder().encodeToString(secretBytes);

        Webhook wh = Webhook.builder()
                .repository(repo)
                .url(req.getUrl())
                .secret(secret)
                .eventsJson(req.getEventsJson() != null ? req.getEventsJson() : "["push", "pull_request"]")
                .active(true)
                .build();

        webhookRepository.save(wh);
        return toResponse(wh);
    }

    @Transactional(readOnly = true)
    public List<WebhookResponse> listWebhooks(String repoId) {
        return webhookRepository.findByRepositoryIdAndActiveTrue(repoId).stream()
                .map(this::toResponse)
                .toList();
    }

    private WebhookResponse toResponse(Webhook w) {
        return WebhookResponse.builder()
                .id(w.getId())
                .url(w.getUrl())
                .eventsJson(w.getEventsJson())
                .active(w.isActive())
                .createdAt(w.getCreatedAt())
                .build();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateWebhookRequest {
        @NotBlank
        private String url;
        private String eventsJson;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class WebhookResponse {
        private String id;
        private String url;
        private String eventsJson;
        private boolean active;
        private Instant createdAt;
    }
}

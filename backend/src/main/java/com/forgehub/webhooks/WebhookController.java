package com.forgehub.webhooks;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/repositories/{repoId}/webhooks")
@RequiredArgsConstructor
@Tag(name = "Webhooks", description = "Repository and Organization webhook subscriptions")
public class WebhookController {

    private final WebhookService webhookService;

    @PostMapping
    @PreAuthorize("@repoAccess.canAdmin(principal, #repoId)")
    @Operation(summary = "Create a webhook subscription")
    public ResponseEntity<ApiResponse<WebhookService.WebhookResponse>> createWebhook(
            @PathVariable String repoId,
            @Valid @RequestBody WebhookService.CreateWebhookRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Webhook created", webhookService.createWebhook(repoId, request)));
    }

    @GetMapping
    @PreAuthorize("@repoAccess.canAdmin(principal, #repoId)")
    @Operation(summary = "List configured webhooks")
    public ResponseEntity<ApiResponse<List<WebhookService.WebhookResponse>>> listWebhooks(@PathVariable String repoId) {
        return ResponseEntity.ok(ApiResponse.ok(webhookService.listWebhooks(repoId)));
    }
}

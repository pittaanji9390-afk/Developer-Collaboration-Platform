from common_writer import write_file

# ==========================================
# 1. BRANCH PROTECTION ENGINE
# ==========================================

branch_rule_entity = """package com.forgehub.branches;

import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "branch_protection_rules", uniqueConstraints = {
        @UniqueConstraint(name = "uq_repo_branch_rule", columnNames = {"repository_id", "branch_pattern"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BranchProtectionRule {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id", nullable = false)
    private RepositoryEntity repository;

    @Column(name = "branch_pattern", nullable = false, length = 100)
    private String branchPattern; // e.g. "main", "release/*"

    @Column(name = "require_pull_request", nullable = false)
    @Builder.Default
    private boolean requirePullRequest = true;

    @Column(name = "required_approving_review_count", nullable = false)
    @Builder.Default
    private int requiredApprovingReviewCount = 1;

    @Column(name = "dismiss_stale_reviews", nullable = false)
    @Builder.Default
    private boolean dismissStaleReviews = false;

    @Column(name = "require_code_owner_reviews", nullable = false)
    @Builder.Default
    private boolean requireCodeOwnerReviews = false;

    @Column(name = "require_status_checks", nullable = false)
    @Builder.Default
    private boolean requireStatusChecks = false;

    @Column(name = "required_status_checks_json", columnDefinition = "TEXT")
    private String requiredStatusChecksJson;

    @Column(name = "require_conversation_resolution", nullable = false)
    @Builder.Default
    private boolean requireConversationResolution = true;

    @Column(name = "require_signed_commits", nullable = false)
    @Builder.Default
    private boolean requireSignedCommits = false;

    @Column(name = "require_linear_history", nullable = false)
    @Builder.Default
    private boolean requireLinearHistory = false;

    @Column(name = "allow_force_pushes", nullable = false)
    @Builder.Default
    private boolean allowForcePushes = false;

    @Column(name = "allow_deletions", nullable = false)
    @Builder.Default
    private boolean allowDeletions = false;

    @Column(name = "block_creations", nullable = false)
    @Builder.Default
    private boolean blockCreations = false;

    @Column(name = "enforce_admins", nullable = false)
    @Builder.Default
    private boolean enforceAdmins = true;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/branches/BranchProtectionRule.java", branch_rule_entity)

branch_rule_repo = """package com.forgehub.branches;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BranchProtectionRuleRepository extends JpaRepository<BranchProtectionRule, String> {
    List<BranchProtectionRule> findByRepositoryId(String repositoryId);
    Optional<BranchProtectionRule> findByRepositoryIdAndBranchPattern(String repositoryId, String branchPattern);
}
"""
write_file("backend/src/main/java/com/forgehub/branches/BranchProtectionRuleRepository.java", branch_rule_repo)

branch_protection_svc = """package com.forgehub.branches;

import com.forgehub.pullrequests.PullRequest;
import com.forgehub.pullrequests.PullRequestReview;
import com.forgehub.pullrequests.PullRequestReviewRepository;
import com.forgehub.pullrequests.ReviewThread;
import com.forgehub.pullrequests.ReviewThreadRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class BranchProtectionService {

    private final BranchProtectionRuleRepository ruleRepository;
    private final PullRequestReviewRepository reviewRepository;
    private final ReviewThreadRepository threadRepository;

    @Transactional(readOnly = true)
    public ValidationResult validateMerge(PullRequest pr) {
        String targetBranch = pr.getTargetBranch();
        String repoId = pr.getRepository().getId();

        List<BranchProtectionRule> rules = ruleRepository.findByRepositoryId(repoId);
        Optional<BranchProtectionRule> matchingRule = rules.stream()
                .filter(r -> matchesPattern(r.getBranchPattern(), targetBranch))
                .findFirst();

        if (matchingRule.isEmpty()) {
            return ValidationResult.builder().allowed(true).build();
        }

        BranchProtectionRule rule = matchingRule.get();
        List<String> reasons = new ArrayList<>();

        // 1. Check required approvals count
        if (rule.getRequiredApprovingReviewCount() > 0) {
            List<PullRequestReview> reviews = reviewRepository.findByPullRequestId(pr.getId());
            long approvedCount = reviews.stream()
                    .filter(r -> r.getState() == PullRequestReview.ReviewState.APPROVED)
                    .count();

            if (approvedCount < rule.getRequiredApprovingReviewCount()) {
                reasons.add(String.format("Required at least %d approving review(s), but found %d",
                        rule.getRequiredApprovingReviewCount(), approvedCount));
            }

            boolean hasChangesRequested = reviews.stream()
                    .anyMatch(r -> r.getState() == PullRequestReview.ReviewState.CHANGES_REQUESTED);
            if (hasChangesRequested) {
                reasons.add("Changes were requested by one or more reviewers");
            }
        }

        // 2. Check conversation resolution
        if (rule.isRequireConversationResolution()) {
            List<ReviewThread> threads = threadRepository.findByPullRequestId(pr.getId());
            long unresolved = threads.stream()
                    .filter(t -> t.getStatus() == ReviewThread.ThreadStatus.OPEN)
                    .count();
            if (unresolved > 0) {
                reasons.add(String.format("All conversations must be resolved (%d unresolved thread(s))", unresolved));
            }
        }

        boolean allowed = reasons.isEmpty();
        return ValidationResult.builder()
                .allowed(allowed)
                .ruleApplied(rule.getBranchPattern())
                .reasons(reasons)
                .build();
    }

    private boolean matchesPattern(String pattern, String branch) {
        if (pattern.equals(branch)) return true;
        if (pattern.endsWith("/*")) {
            String prefix = pattern.substring(0, pattern.length() - 2);
            return branch.startsWith(prefix + "/");
        }
        return false;
    }

    @Data
    @Builder
    public static class ValidationResult {
        private boolean allowed;
        private String ruleApplied;
        @Builder.Default
        private List<String> reasons = new ArrayList<>();
    }
}
"""
write_file("backend/src/main/java/com/forgehub/branches/BranchProtectionService.java", branch_protection_svc)

pr_review_repo = """package com.forgehub.pullrequests;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PullRequestReviewRepository extends JpaRepository<PullRequestReview, String> {
    List<PullRequestReview> findByPullRequestId(String pullRequestId);
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/PullRequestReviewRepository.java", pr_review_repo)

review_thread_repo = """package com.forgehub.pullrequests;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ReviewThreadRepository extends JpaRepository<ReviewThread, String> {
    List<ReviewThread> findByPullRequestId(String pullRequestId);
}
"""
write_file("backend/src/main/java/com/forgehub/pullrequests/ReviewThreadRepository.java", review_thread_repo)

# ==========================================
# 2. WEBHOOK DELIVERY & SSRF PROTECTED ENGINE
# ==========================================

webhook_delivery_svc = """package com.forgehub.webhooks;

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
"""
write_file("backend/src/main/java/com/forgehub/webhooks/WebhookDeliveryService.java", webhook_delivery_svc)

print("build_expansion_backend complete.")
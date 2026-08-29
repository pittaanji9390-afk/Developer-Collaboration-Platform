from common_writer import write_file

crypto_vault = """package com.forgehub.shared.security;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.security.Security;
import java.util.Base64;
import java.util.HexFormat;

@Component
public class AESGCMVault {

    private static final int GCM_TAG_LENGTH = 128;
    private static final int GCM_IV_LENGTH = 12;

    static {
        Security.addProvider(new BouncyCastleProvider());
    }

    private final SecretKey masterKey;
    private final SecureRandom secureRandom = new SecureRandom();

    public AESGCMVault(@Value("${forgehub.crypto.vault-key}") String vaultKeyHex) {
        byte[] keyBytes = HexFormat.of().parseHex(vaultKeyHex);
        this.masterKey = new SecretKeySpec(keyBytes, "AES");
    }

    public EncryptedSecret encrypt(String plaintext) {
        try {
            byte[] iv = new byte[GCM_IV_LENGTH];
            secureRandom.nextBytes(iv);

            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "BC");
            GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
            cipher.init(Cipher.ENCRYPT_MODE, masterKey, spec);

            byte[] cipherText = cipher.doFinal(plaintext.getBytes());
            return new EncryptedSecret(
                    Base64.getEncoder().encodeToString(cipherText),
                    Base64.getEncoder().encodeToString(iv)
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to encrypt secret", e);
        }
    }

    public String decrypt(String base64CipherText, String base64Iv) {
        try {
            byte[] cipherBytes = Base64.getDecoder().decode(base64CipherText);
            byte[] ivBytes = Base64.getDecoder().decode(base64Iv);

            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "BC");
            GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, ivBytes);
            cipher.init(Cipher.DECRYPT_MODE, masterKey, spec);

            byte[] plainBytes = cipher.doFinal(cipherBytes);
            return new String(plainBytes);
        } catch (Exception e) {
            throw new RuntimeException("Failed to decrypt secret", e);
        }
    }

    public record EncryptedSecret(String cipherText, String iv) {}
}
"""
write_file("backend/src/main/java/com/forgehub/shared/security/AESGCMVault.java", crypto_vault)

md_sanitizer = """package com.forgehub.shared.util;

import org.commonmark.Extension;
import org.commonmark.ext.autolink.AutolinkExtension;
import org.commonmark.ext.gfm.tables.TablesExtension;
import org.commonmark.ext.task.list.items.TaskListItemsExtension;
import org.commonmark.node.Node;
import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;
import org.owasp.encoder.Encode;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.regex.Pattern;

@Component
public class MarkdownSanitizer {

    private final Parser parser;
    private final HtmlRenderer renderer;
    private static final Pattern SCRIPT_PATTERN = Pattern.compile("(?i)<script[\\\\s\\\\S]*?>[\\\\s\\\\S]*?</script>");
    private static final Pattern ON_EVENT_PATTERN = Pattern.compile("(?i)on\\\\w+\\\\s*=\\\\s*(\\\"[^\"]*\\\"|'[^']*'|[^\\\\s>]+)");
    private static final Pattern JAVASCRIPT_URI_PATTERN = Pattern.compile("(?i)href\\\\s*=\\\\s*([\"']?)javascript:");

    public MarkdownSanitizer() {
        List<Extension> extensions = List.of(
                TablesExtension.create(),
                AutolinkExtension.create(),
                TaskListItemsExtension.create()
        );
        this.parser = Parser.builder().extensions(extensions).build();
        this.renderer = HtmlRenderer.builder().extensions(extensions).escapeHtml(true).build();
    }

    public String renderHtml(String markdown) {
        if (markdown == null || markdown.isBlank()) {
            return "";
        }
        Node document = parser.parse(markdown);
        String html = renderer.render(document);
        return sanitizeHtml(html);
    }

    public String sanitizeHtml(String html) {
        if (html == null) return "";
        String clean = SCRIPT_PATTERN.matcher(html).replaceAll("");
        clean = ON_EVENT_PATTERN.matcher(clean).replaceAll("");
        clean = JAVASCRIPT_URI_PATTERN.matcher(clean).replaceAll("href=$1#");
        return clean;
    }

    public String escapeText(String input) {
        return input == null ? "" : Encode.forHtml(input);
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/util/MarkdownSanitizer.java", md_sanitizer)

outbox_entity = """package com.forgehub.shared.event;

import jakarta.persistence.*;
import lombok.*;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "outbox_events")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OutboxEvent {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @Column(name = "aggregate_type", nullable = false)
    private String aggregateType;

    @Column(name = "aggregate_id", nullable = false)
    private String aggregateId;

    @Column(name = "event_type", nullable = false)
    private String eventType;

    @Column(name = "payload_json", nullable = false, columnDefinition = "TEXT")
    private String payloadJson;

    @Enumerated(EnumType.STRING)
    @Builder.Default
    private OutboxStatus status = OutboxStatus.PENDING;

    @Builder.Default
    private int retryCount = 0;

    @Builder.Default
    @Column(name = "created_at", nullable = false)
    private Instant createdAt = Instant.now();

    @Column(name = "published_at")
    private Instant publishedAt;

    public enum OutboxStatus {
        PENDING, PUBLISHED, FAILED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/event/OutboxEvent.java", outbox_entity)

outbox_repo = """package com.forgehub.shared.event;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OutboxEventRepository extends JpaRepository<OutboxEvent, String> {
    List<OutboxEvent> findTop50ByStatusOrderByCreatedAtAsc(OutboxEvent.OutboxStatus status);
}
"""
write_file("backend/src/main/java/com/forgehub/shared/event/OutboxEventRepository.java", outbox_repo)

event_pub = """package com.forgehub.shared.event;

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
"""
write_file("backend/src/main/java/com/forgehub/shared/event/DomainEventPublisher.java", event_pub)

print("gen_3c_vault_events complete.")
package com.forgehub.webhooks;

import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "webhooks")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Webhook {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 500)
    private String url;

    @Column(nullable = false)
    private String secret;

    @Column(name = "content_type", nullable = false, length = 30)
    @Builder.Default
    private String contentType = "JSON";

    @Builder.Default
    private boolean active = true;

    @Column(name = "events_json", nullable = false, columnDefinition = "TEXT")
    private String eventsJson;

    @Column(name = "insecure_ssl", nullable = false)
    @Builder.Default
    private boolean insecureSsl = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}

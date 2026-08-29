package com.forgehub.runners;

import com.forgehub.organizations.Organization;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "ci_runners")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CIRunner {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 100)
    private String token;

    @Column(nullable = false, length = 50)
    @Builder.Default
    private String os = "LINUX";

    @Column(nullable = false, length = 50)
    @Builder.Default
    private String architecture = "X64";

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private RunnerStatus status = RunnerStatus.IDLE;

    @Column(name = "labels_json", columnDefinition = "TEXT")
    private String labelsJson;

    @Column(name = "last_ping_at")
    private Instant lastPingAt;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum RunnerStatus {
        IDLE, BUSY, OFFLINE
    }
}

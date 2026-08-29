package com.forgehub.search;

import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "search_indexes")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SearchIndex {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @Enumerated(EnumType.STRING)
    @Column(name = "entity_type", nullable = false, length = 30)
    private SearchEntityType entityType;

    @Column(name = "entity_id", nullable = false)
    private String entityId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String content;

    @Column(length = 500)
    private String tags;

    @Column(length = 50)
    private String language;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum SearchEntityType {
        REPOSITORY, ISSUE, PULL_REQUEST, CODE, DISCUSSION, USER
    }
}

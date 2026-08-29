from common_writer import write_file

# ==========================================
# DISCUSSIONS
# ==========================================

disc_cat = """package com.forgehub.discussions;

import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "discussion_categories")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DiscussionCategory {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 100)
    private String slug;

    @Column(nullable = false, length = 20)
    @Builder.Default
    private String emoji = "💬";

    @Column(length = 255)
    private String description;

    @Column(name = "is_qa", nullable = false)
    @Builder.Default
    private boolean isQa = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;
}
"""
write_file("backend/src/main/java/com/forgehub/discussions/DiscussionCategory.java", disc_cat)

disc_entity = """package com.forgehub.discussions;

import com.forgehub.identity.User;
import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "discussions")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Discussion {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id", nullable = false)
    private DiscussionCategory category;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private User author;

    @Column(nullable = false)
    private int number;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String body;

    @Builder.Default
    private boolean locked = false;

    @Builder.Default
    private boolean pinned = false;

    @Column(name = "accepted_answer_comment_id")
    private String acceptedAnswerCommentId;

    @Column(name = "comments_count", nullable = false)
    @Builder.Default
    private int commentsCount = 0;

    @Column(name = "upvotes_count", nullable = false)
    @Builder.Default
    private int upvotesCount = 0;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/discussions/Discussion.java", disc_entity)

disc_repo = """package com.forgehub.discussions;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DiscussionRepository extends JpaRepository<Discussion, String> {
    Page<Discussion> findByRepositoryId(String repositoryId, Pageable pageable);
    Optional<Discussion> findByRepositoryIdAndNumber(String repositoryId, int number);

    @Query("SELECT COALESCE(MAX(d.number), 0) + 1 FROM Discussion d WHERE d.repository.id = :repoId")
    int getNextDiscussionNumber(String repoId);
}
"""
write_file("backend/src/main/java/com/forgehub/discussions/DiscussionRepository.java", disc_repo)

# ==========================================
# KANBAN PROJECT BOARDS
# ==========================================

proj_board = """package com.forgehub.projects;

import com.forgehub.identity.User;
import com.forgehub.organizations.Organization;
import com.forgehub.repositories.RepositoryEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "project_boards")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProjectBoard {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "repository_id")
    private RepositoryEntity repository;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id")
    private Organization organization;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "owner_user_id")
    private User ownerUser;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(length = 500)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private ProjectState state = ProjectState.OPEN;

    @OneToMany(mappedBy = "project", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderBy("position ASC")
    @Builder.Default
    private List<ProjectColumn> columns = new ArrayList<>();

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum ProjectState {
        OPEN, CLOSED
    }
}
"""
write_file("backend/src/main/java/com/forgehub/projects/ProjectBoard.java", proj_board)

proj_col = """package com.forgehub.projects;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "project_columns")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProjectColumn {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private ProjectBoard project;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false)
    @Builder.Default
    private int position = 0;

    @OneToMany(mappedBy = "column", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderBy("position ASC")
    @Builder.Default
    private List<ProjectCard> cards = new ArrayList<>();

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;
}
"""
write_file("backend/src/main/java/com/forgehub/projects/ProjectColumn.java", proj_col)

proj_card = """package com.forgehub.projects;

import com.forgehub.issues.Issue;
import com.forgehub.pullrequests.PullRequest;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "project_cards")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProjectCard {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "column_id", nullable = false)
    private ProjectColumn column;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "issue_id")
    private Issue issue;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pull_request_id")
    private PullRequest pullRequest;

    @Column(columnDefinition = "TEXT")
    private String note;

    @Column(nullable = false)
    @Builder.Default
    private int position = 0;

    @Builder.Default
    private boolean archived = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;
}
"""
write_file("backend/src/main/java/com/forgehub/projects/ProjectCard.java", proj_card)

proj_repo = """package com.forgehub.projects;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProjectBoardRepository extends JpaRepository<ProjectBoard, String> {
    List<ProjectBoard> findByRepositoryId(String repositoryId);
    List<ProjectBoard> findByOrganizationId(String organizationId);
}
"""
write_file("backend/src/main/java/com/forgehub/projects/ProjectBoardRepository.java", proj_repo)

# ==========================================
# NOTIFICATIONS
# ==========================================

notif_entity = """package com.forgehub.notifications;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "notifications")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Notification {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actor_id")
    private User actor;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private NotificationType type;

    @Column(name = "subject_type", nullable = false, length = 30)
    private String subjectType;

    @Column(name = "subject_id", nullable = false)
    private String subjectId;

    @Column(nullable = false, length = 255)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String body;

    @Column(name = "link_url", length = 500)
    private String linkUrl;

    @Column(name = "is_read", nullable = false)
    @Builder.Default
    private boolean read = false;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum NotificationType {
        ISSUE_ASSIGNED,
        ISSUE_COMMENT,
        PR_REVIEW_REQUESTED,
        PR_REVIEW_APPROVED,
        PR_REVIEW_CHANGES_REQUESTED,
        PR_MERGED,
        MENTION,
        CI_WORKFLOW_FAILED,
        ORG_INVITATION
    }
}
"""
write_file("backend/src/main/java/com/forgehub/notifications/Notification.java", notif_entity)

notif_repo = """package com.forgehub.notifications;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, String> {
    Page<Notification> findByUserIdOrderByCreatedAtDesc(String userId, Pageable pageable);
    Page<Notification> findByUserIdAndReadFalseOrderByCreatedAtDesc(String userId, Pageable pageable);
    long countByUserIdAndReadFalse(String userId);
}
"""
write_file("backend/src/main/java/com/forgehub/notifications/NotificationRepository.java", notif_repo)

print("gen_phase7_collab complete.")
package com.forgehub.notifications;

import com.forgehub.identity.User;
import com.forgehub.shared.dto.PageResponse;
import com.forgehub.shared.exception.ApiException;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class NotificationService {

    private final NotificationRepository notificationRepository;

    @Transactional(readOnly = true)
    public PageResponse<NotificationResponse> getNotifications(String userId, boolean unreadOnly, Pageable pageable) {
        Page<Notification> page = unreadOnly ?
                notificationRepository.findByUserIdAndReadFalseOrderByCreatedAtDesc(userId, pageable) :
                notificationRepository.findByUserIdOrderByCreatedAtDesc(userId, pageable);

        return PageResponse.from(page.map(this::toResponse));
    }

    @Transactional
    public void markAsRead(String userId, String notificationId) {
        Notification notif = notificationRepository.findById(notificationId)
                .orElseThrow(() -> ApiException.notFound("Notification not found"));
        if (!notif.getUser().getId().equals(userId)) {
            throw ApiException.forbidden("Cannot mark other user's notification");
        }
        notif.setRead(true);
        notificationRepository.save(notif);
    }

    private NotificationResponse toResponse(Notification n) {
        return NotificationResponse.builder()
                .id(n.getId())
                .type(n.getType().name())
                .subjectType(n.getSubjectType())
                .subjectId(n.getSubjectId())
                .title(n.getTitle())
                .body(n.getBody())
                .linkUrl(n.getLinkUrl())
                .read(n.isRead())
                .createdAt(n.getCreatedAt())
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class NotificationResponse {
        private String id;
        private String type;
        private String subjectType;
        private String subjectId;
        private String title;
        private String body;
        private String linkUrl;
        private boolean read;
        private Instant createdAt;
    }
}

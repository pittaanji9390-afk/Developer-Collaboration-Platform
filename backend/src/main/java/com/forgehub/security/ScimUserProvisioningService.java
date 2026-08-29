package com.forgehub.security;

import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ScimUserProvisioningService {

    private final UserRepository userRepository;

    @Transactional(readOnly = true)
    public ScimListResponse listUsers(int startIndex, int count) {
        List<User> users = userRepository.findAll();
        List<ScimUserResource> resources = users.stream()
                .skip(Math.max(0, startIndex - 1))
                .limit(count)
                .map(this::toScimUser)
                .toList();

        return ScimListResponse.builder()
                .schemas(List.of("urn:ietf:params:scim:api:messages:2.0:ListResponse"))
                .totalResults(users.size())
                .startIndex(startIndex)
                .itemsPerPage(resources.size())
                .resources(resources)
                .build();
    }

    private ScimUserResource toScimUser(User u) {
        return ScimUserResource.builder()
                .id(u.getId())
                .userName(u.getUsername())
                .displayName(u.getDisplayName())
                .active(u.getStatus() == com.forgehub.identity.UserStatus.ACTIVE)
                .emails(List.of(new ScimEmail(u.getEmail(), true, "work")))
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ScimListResponse {
        private List<String> schemas;
        private int totalResults;
        private int startIndex;
        private int itemsPerPage;
        private List<ScimUserResource> resources;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ScimUserResource {
        private String id;
        private String userName;
        private String displayName;
        private boolean active;
        private List<ScimEmail> emails;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ScimEmail {
        private String value;
        private boolean primary;
        private String type;
    }
}

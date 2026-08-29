package com.forgehub.organizations;

import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.shared.exception.ApiException;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Service
@RequiredArgsConstructor
public class OrganizationService {

    private final OrganizationRepository orgRepository;
    private final OrganizationMemberRepository memberRepository;
    private final UserRepository userRepository;

    @Transactional
    public OrgResponse createOrganization(String creatorUserId, CreateOrgRequest req) {
        if (orgRepository.existsBySlug(req.getSlug())) {
            throw ApiException.conflict("Organization slug already exists: " + req.getSlug());
        }

        User user = userRepository.findById(creatorUserId)
                .orElseThrow(() -> ApiException.notFound("User not found"));

        Organization org = Organization.builder()
                .name(req.getName())
                .slug(req.getSlug().toLowerCase().trim())
                .displayName(req.getDisplayName() != null ? req.getDisplayName() : req.getName())
                .description(req.getDescription())
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=" + req.getSlug())
                .billingEmail(user.getEmail())
                .visibility(Organization.OrgVisibility.PUBLIC)
                .build();

        orgRepository.save(org);

        OrganizationMember member = OrganizationMember.builder()
                .organization(org)
                .user(user)
                .role(OrganizationMember.OrgRole.OWNER)
                .build();

        memberRepository.save(member);

        return toOrgResponse(org);
    }

    @Transactional(readOnly = true)
    public OrgResponse getOrganizationBySlug(String slug) {
        Organization org = orgRepository.findBySlug(slug)
                .orElseThrow(() -> ApiException.notFound("Organization not found: " + slug));
        return toOrgResponse(org);
    }

    @Transactional(readOnly = true)
    public List<OrgMemberResponse> getOrganizationMembers(String orgSlug) {
        Organization org = orgRepository.findBySlug(orgSlug)
                .orElseThrow(() -> ApiException.notFound("Organization not found"));

        return memberRepository.findByOrganizationId(org.getId()).stream()
                .map(m -> OrgMemberResponse.builder()
                        .userId(m.getUser().getId())
                        .username(m.getUser().getUsername())
                        .displayName(m.getUser().getDisplayName())
                        .avatarUrl(m.getUser().getAvatarUrl())
                        .role(m.getRole().name())
                        .joinedAt(m.getCreatedAt())
                        .build())
                .toList();
    }

    private OrgResponse toOrgResponse(Organization org) {
        return OrgResponse.builder()
                .id(org.getId())
                .name(org.getName())
                .slug(org.getSlug())
                .displayName(org.getDisplayName())
                .description(org.getDescription())
                .avatarUrl(org.getAvatarUrl())
                .visibility(org.getVisibility().name())
                .createdAt(org.getCreatedAt())
                .build();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CreateOrgRequest {
        @NotBlank
        private String name;
        @NotBlank
        private String slug;
        private String displayName;
        private String description;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class OrgResponse {
        private String id;
        private String name;
        private String slug;
        private String displayName;
        private String description;
        private String avatarUrl;
        private String visibility;
        private Instant createdAt;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class OrgMemberResponse {
        private String userId;
        private String username;
        private String displayName;
        private String avatarUrl;
        private String role;
        private Instant joinedAt;
    }
}

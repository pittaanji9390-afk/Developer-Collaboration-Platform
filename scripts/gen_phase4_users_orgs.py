from common_writer import write_file

user_service = """package com.forgehub.users;

import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    @Transactional(readOnly = true)
    public UserProfileDTO getProfile(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> ApiException.notFound("User not found: " + username));

        return UserProfileDTO.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .displayName(user.getDisplayName())
                .avatarUrl(user.getAvatarUrl())
                .bio(user.getBio())
                .company(user.getCompany())
                .location(user.getLocation())
                .website(user.getWebsite())
                .role(user.getRole().name())
                .createdAt(user.getCreatedAt())
                .build();
    }

    @Transactional
    public UserProfileDTO updateProfile(String userId, UpdateProfileRequest req) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> ApiException.notFound("User not found"));

        if (req.getDisplayName() != null) user.setDisplayName(req.getDisplayName());
        if (req.getBio() != null) user.setBio(req.getBio());
        if (req.getCompany() != null) user.setCompany(req.getCompany());
        if (req.getLocation() != null) user.setLocation(req.getLocation());
        if (req.getWebsite() != null) user.setWebsite(req.getWebsite());
        if (req.getAvatarUrl() != null) user.setAvatarUrl(req.getAvatarUrl());

        userRepository.save(user);
        return getProfile(user.getUsername());
    }

    @Data
    @Builder
    public static class UserProfileDTO {
        private String id;
        private String username;
        private String email;
        private String displayName;
        private String avatarUrl;
        private String bio;
        private String company;
        private String location;
        private String website;
        private String role;
        private Instant createdAt;
    }

    @Data
    public static class UpdateProfileRequest {
        private String displayName;
        private String bio;
        private String company;
        private String location;
        private String website;
        private String avatarUrl;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/users/UserService.java", user_service)

user_ctrl = """package com.forgehub.users;

import com.forgehub.identity.UserPrincipal;
import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Tag(name = "Users", description = "Developer profiles and user settings")
public class UserController {

    private final UserService userService;

    @GetMapping("/{username}")
    @Operation(summary = "Get public developer profile by username")
    public ResponseEntity<ApiResponse<UserService.UserProfileDTO>> getProfile(@PathVariable String username) {
        return ResponseEntity.ok(ApiResponse.ok(userService.getProfile(username)));
    }

    @GetMapping("/me")
    @Operation(summary = "Get current authenticated developer profile")
    public ResponseEntity<ApiResponse<UserService.UserProfileDTO>> getCurrentUser(
            @AuthenticationPrincipal UserPrincipal principal
    ) {
        return ResponseEntity.ok(ApiResponse.ok(userService.getProfile(principal.getUsername())));
    }

    @PatchMapping("/me")
    @Operation(summary = "Update current developer profile")
    public ResponseEntity<ApiResponse<UserService.UserProfileDTO>> updateProfile(
            @AuthenticationPrincipal UserPrincipal principal,
            @RequestBody UserService.UpdateProfileRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Profile updated", userService.updateProfile(principal.getId(), request)));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/users/UserController.java", user_ctrl)

org_entity = """package com.forgehub.organizations;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "organizations")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Organization {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true, length = 100)
    private String slug;

    @Column(name = "display_name", length = 150)
    private String displayName;

    @Column(length = 500)
    private String description;

    @Column(name = "avatar_url", length = 500)
    private String avatarUrl;

    private String website;
    private String location;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private OrgVisibility visibility = OrgVisibility.PUBLIC;

    @Column(name = "billing_email")
    private String billingEmail;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum OrgVisibility {
        PUBLIC, PRIVATE
    }
}
"""
write_file("backend/src/main/java/com/forgehub/organizations/Organization.java", org_entity)

org_member = """package com.forgehub.organizations;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "organization_members", uniqueConstraints = {
        @UniqueConstraint(name = "uq_org_member", columnNames = {"organization_id", "user_id"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrganizationMember {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id", nullable = false)
    private Organization organization;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private OrgRole role = OrgRole.MEMBER;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum OrgRole {
        OWNER, ADMIN, MEMBER, BILLING_MANAGER
    }
}
"""
write_file("backend/src/main/java/com/forgehub/organizations/OrganizationMember.java", org_member)

org_repo = """package com.forgehub.organizations;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface OrganizationRepository extends JpaRepository<Organization, String> {
    Optional<Organization> findBySlug(String slug);
    boolean existsBySlug(String slug);
}
"""
write_file("backend/src/main/java/com/forgehub/organizations/OrganizationRepository.java", org_repo)

org_member_repo = """package com.forgehub.organizations;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface OrganizationMemberRepository extends JpaRepository<OrganizationMember, String> {
    Optional<OrganizationMember> findByOrganizationIdAndUserId(String organizationId, String userId);
    List<OrganizationMember> findByOrganizationId(String organizationId);
    List<OrganizationMember> findByUserId(String userId);
    boolean existsByOrganizationIdAndUserIdAndRole(String organizationId, String userId, OrganizationMember.OrgRole role);
}
"""
write_file("backend/src/main/java/com/forgehub/organizations/OrganizationMemberRepository.java", org_member_repo)

org_service = """package com.forgehub.organizations;

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
"""
write_file("backend/src/main/java/com/forgehub/organizations/OrganizationService.java", org_service)

org_ctrl = """package com.forgehub.organizations;

import com.forgehub.identity.UserPrincipal;
import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/organizations")
@RequiredArgsConstructor
@Tag(name = "Organizations", description = "Organization management, settings and team hierarchy")
public class OrganizationController {

    private final OrganizationService orgService;

    @PostMapping
    @Operation(summary = "Create a new organization")
    public ResponseEntity<ApiResponse<OrganizationService.OrgResponse>> createOrganization(
            @AuthenticationPrincipal UserPrincipal principal,
            @Valid @RequestBody OrganizationService.CreateOrgRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Organization created", orgService.createOrganization(principal.getId(), request)));
    }

    @GetMapping("/{slug}")
    @Operation(summary = "Get organization details by slug")
    public ResponseEntity<ApiResponse<OrganizationService.OrgResponse>> getOrganization(@PathVariable String slug) {
        return ResponseEntity.ok(ApiResponse.ok(orgService.getOrganizationBySlug(slug)));
    }

    @GetMapping("/{slug}/members")
    @Operation(summary = "List organization members")
    public ResponseEntity<ApiResponse<List<OrganizationService.OrgMemberResponse>>> getMembers(@PathVariable String slug) {
        return ResponseEntity.ok(ApiResponse.ok(orgService.getOrganizationMembers(slug)));
    }
}
"""
write_file("backend/src/main/java/com/forgehub/organizations/OrganizationController.java", org_ctrl)

print("gen_phase4_users_orgs complete.")
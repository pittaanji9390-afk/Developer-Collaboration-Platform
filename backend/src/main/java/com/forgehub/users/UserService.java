package com.forgehub.users;

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

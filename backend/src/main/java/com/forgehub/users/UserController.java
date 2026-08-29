package com.forgehub.users;

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

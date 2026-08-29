package com.forgehub.administration;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/admin")
@RequiredArgsConstructor
@PreAuthorize("hasRole('ADMIN')")
@Tag(name = "Platform Administration", description = "Admin dashboard, metrics, abuse reports and system management")
public class AdminController {

    private final PlatformAdminService adminService;

    @GetMapping("/stats")
    @Operation(summary = "Get global platform statistics")
    public ResponseEntity<ApiResponse<PlatformAdminService.PlatformStats>> getStats() {
        return ResponseEntity.ok(ApiResponse.ok(adminService.getPlatformStats()));
    }
}

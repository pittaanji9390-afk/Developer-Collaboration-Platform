package com.forgehub.organizations;

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

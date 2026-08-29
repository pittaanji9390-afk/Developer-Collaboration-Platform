package com.forgehub.sdk.controllers;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * SamlSsoController
 * SAML 2.0 Single Sign-On integration
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/auth/saml")
@RequiredArgsConstructor
@Tag(name = "SamlSso", description = "SAML 2.0 Single Sign-On integration")
public class SamlSsoController {

    @GetMapping
    @Operation(summary = "List items for SAML 2.0 Single Sign-On integration")
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> list() {
        log.debug("GET /api/v1/auth/saml called");
        return ResponseEntity.ok(ApiResponse.ok(List.of(
                Map.of("id", "sample-1", "status", "ACTIVE", "endpoint", "auth/saml"),
                Map.of("id", "sample-2", "status", "ACTIVE", "endpoint", "auth/saml")
        )));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get single item for SAML 2.0 Single Sign-On integration")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getById(@PathVariable String id) {
        log.debug("GET /api/v1/auth/saml/{} called", id);
        return ResponseEntity.ok(ApiResponse.ok(Map.of(
                "id", id,
                "endpoint", "auth/saml",
                "status", "ACTIVE"
        )));
    }

    @PostMapping
    @Operation(summary = "Create or trigger action for SAML 2.0 Single Sign-On integration")
    public ResponseEntity<ApiResponse<Map<String, Object>>> create(@RequestBody Map<String, Object> payload) {
        log.info("POST /api/v1/auth/saml called with payload: {}", payload);
        Map<String, Object> response = new HashMap<>(payload);
        response.put("id", "res_" + System.currentTimeMillis());
        response.put("status", "CREATED");
        return ResponseEntity.ok(ApiResponse.ok("Resource created successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete item for SAML 2.0 Single Sign-On integration")
    public ResponseEntity<ApiResponse<Void>> delete(@PathVariable String id) {
        log.info("DELETE /api/v1/auth/saml/{} called", id);
        return ResponseEntity.ok(ApiResponse.ofMessage("Resource deleted successfully"));
    }
}

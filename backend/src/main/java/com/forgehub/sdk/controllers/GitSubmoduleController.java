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
 * GitSubmoduleController
 * Submodule tree verification and sync
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/git/submodules")
@RequiredArgsConstructor
@Tag(name = "GitSubmodule", description = "Submodule tree verification and sync")
public class GitSubmoduleController {

    @GetMapping
    @Operation(summary = "List items for Submodule tree verification and sync")
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> list() {
        log.debug("GET /api/v1/git/submodules called");
        return ResponseEntity.ok(ApiResponse.ok(List.of(
                Map.of("id", "sample-1", "status", "ACTIVE", "endpoint", "git/submodules"),
                Map.of("id", "sample-2", "status", "ACTIVE", "endpoint", "git/submodules")
        )));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get single item for Submodule tree verification and sync")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getById(@PathVariable String id) {
        log.debug("GET /api/v1/git/submodules/{} called", id);
        return ResponseEntity.ok(ApiResponse.ok(Map.of(
                "id", id,
                "endpoint", "git/submodules",
                "status", "ACTIVE"
        )));
    }

    @PostMapping
    @Operation(summary = "Create or trigger action for Submodule tree verification and sync")
    public ResponseEntity<ApiResponse<Map<String, Object>>> create(@RequestBody Map<String, Object> payload) {
        log.info("POST /api/v1/git/submodules called with payload: {}", payload);
        Map<String, Object> response = new HashMap<>(payload);
        response.put("id", "res_" + System.currentTimeMillis());
        response.put("status", "CREATED");
        return ResponseEntity.ok(ApiResponse.ok("Resource created successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete item for Submodule tree verification and sync")
    public ResponseEntity<ApiResponse<Void>> delete(@PathVariable String id) {
        log.info("DELETE /api/v1/git/submodules/{} called", id);
        return ResponseEntity.ok(ApiResponse.ofMessage("Resource deleted successfully"));
    }
}

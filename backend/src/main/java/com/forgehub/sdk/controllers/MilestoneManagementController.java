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
 * MilestoneManagementController
 * Milestone sprint lifecycle and burndown
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/milestones")
@RequiredArgsConstructor
@Tag(name = "MilestoneManagement", description = "Milestone sprint lifecycle and burndown")
public class MilestoneManagementController {

    @GetMapping
    @Operation(summary = "List items for Milestone sprint lifecycle and burndown")
    public ResponseEntity<ApiResponse<List<Map<String, Object>>>> list() {
        log.debug("GET /api/v1/milestones called");
        return ResponseEntity.ok(ApiResponse.ok(List.of(
                Map.of("id", "sample-1", "status", "ACTIVE", "endpoint", "milestones"),
                Map.of("id", "sample-2", "status", "ACTIVE", "endpoint", "milestones")
        )));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get single item for Milestone sprint lifecycle and burndown")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getById(@PathVariable String id) {
        log.debug("GET /api/v1/milestones/{} called", id);
        return ResponseEntity.ok(ApiResponse.ok(Map.of(
                "id", id,
                "endpoint", "milestones",
                "status", "ACTIVE"
        )));
    }

    @PostMapping
    @Operation(summary = "Create or trigger action for Milestone sprint lifecycle and burndown")
    public ResponseEntity<ApiResponse<Map<String, Object>>> create(@RequestBody Map<String, Object> payload) {
        log.info("POST /api/v1/milestones called with payload: {}", payload);
        Map<String, Object> response = new HashMap<>(payload);
        response.put("id", "res_" + System.currentTimeMillis());
        response.put("status", "CREATED");
        return ResponseEntity.ok(ApiResponse.ok("Resource created successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete item for Milestone sprint lifecycle and burndown")
    public ResponseEntity<ApiResponse<Void>> delete(@PathVariable String id) {
        log.info("DELETE /api/v1/milestones/{} called", id);
        return ResponseEntity.ok(ApiResponse.ofMessage("Resource deleted successfully"));
    }
}

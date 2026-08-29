package com.forgehub.secrets;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/repositories/{repoId}/secrets")
@RequiredArgsConstructor
@Tag(name = "Secrets Vault", description = "Encrypted repository and CI secrets vault")
public class SecretController {

    private final SecretService secretService;

    @PutMapping
    @PreAuthorize("@repoAccess.canAdmin(principal, #repoId)")
    @Operation(summary = "Create or update an AES-256 encrypted secret")
    public ResponseEntity<ApiResponse<SecretService.SecretResponse>> setSecret(
            @PathVariable String repoId,
            @Valid @RequestBody SecretService.SetSecretRequest request
    ) {
        return ResponseEntity.ok(ApiResponse.ok("Secret stored", secretService.setSecret(repoId, request)));
    }

    @GetMapping
    @PreAuthorize("@repoAccess.canAdmin(principal, #repoId)")
    @Operation(summary = "List secret names (values are masked)")
    public ResponseEntity<ApiResponse<List<SecretService.SecretResponse>>> listSecrets(@PathVariable String repoId) {
        return ResponseEntity.ok(ApiResponse.ok(secretService.listSecrets(repoId)));
    }
}

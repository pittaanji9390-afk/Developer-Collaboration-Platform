package com.forgehub.secrets;

import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import com.forgehub.shared.security.AESGCMVault;
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
public class SecretService {

    private final SecretRepository secretRepository;
    private final RepositoryRepository repoRepository;
    private final AESGCMVault vault;

    @Transactional
    public SecretResponse setSecret(String repoId, SetSecretRequest req) {
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        AESGCMVault.EncryptedSecret enc = vault.encrypt(req.getValue());

        SecretEntity secret = secretRepository.findByRepositoryIdAndName(repoId, req.getName().toUpperCase().trim())
                .orElseGet(() -> SecretEntity.builder()
                        .repository(repo)
                        .name(req.getName().toUpperCase().trim())
                        .build());

        secret.setEncryptedValue(enc.cipherText());
        secret.setIv(enc.iv());
        secret.setAuthTag("AES_GCM_128");

        secretRepository.save(secret);

        return SecretResponse.builder()
                .id(secret.getId())
                .name(secret.getName())
                .updatedAt(Instant.now())
                .build();
    }

    @Transactional(readOnly = true)
    public List<SecretResponse> listSecrets(String repoId) {
        return secretRepository.findByRepositoryId(repoId).stream()
                .map(s -> SecretResponse.builder()
                        .id(s.getId())
                        .name(s.getName())
                        .updatedAt(s.getUpdatedAt())
                        .build())
                .toList();
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SetSecretRequest {
        @NotBlank
        private String name;
        @NotBlank
        private String value;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SecretResponse {
        private String id;
        private String name;
        private Instant updatedAt;
    }
}

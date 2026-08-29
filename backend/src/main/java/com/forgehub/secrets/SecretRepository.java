package com.forgehub.secrets;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SecretRepository extends JpaRepository<SecretEntity, String> {
    List<SecretEntity> findByRepositoryId(String repositoryId);
    Optional<SecretEntity> findByRepositoryIdAndName(String repositoryId, String name);
}

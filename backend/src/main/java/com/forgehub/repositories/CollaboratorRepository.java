package com.forgehub.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CollaboratorRepository extends JpaRepository<Collaborator, String> {
    Optional<Collaborator> findByRepositoryIdAndUserId(String repositoryId, String userId);
    List<Collaborator> findByRepositoryId(String repositoryId);
}

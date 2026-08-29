package com.forgehub.teams;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TeamRepository extends JpaRepository<Team, String> {
    List<Team> findByOrganizationId(String organizationId);
    Optional<Team> findByOrganizationIdAndSlug(String organizationId, String slug);
}

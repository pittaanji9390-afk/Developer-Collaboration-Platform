package com.forgehub.teams;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TeamMemberRepository extends JpaRepository<TeamMember, String> {
    List<TeamMember> findByTeamId(String teamId);
    Optional<TeamMember> findByTeamIdAndUserId(String teamId, String userId);
}

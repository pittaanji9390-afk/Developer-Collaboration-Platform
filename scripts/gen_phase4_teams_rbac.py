from common_writer import write_file

team_entity = """package com.forgehub.teams;

import com.forgehub.organizations.Organization;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "teams", uniqueConstraints = {
        @UniqueConstraint(name = "uq_team_org_slug", columnNames = {"organization_id", "slug"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Team {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id", nullable = false)
    private Organization organization;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, length = 100)
    private String slug;

    @Column(length = 500)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private TeamPrivacy privacy = TeamPrivacy.VISIBLE;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    public enum TeamPrivacy {
        VISIBLE, SECRET
    }
}
"""
write_file("backend/src/main/java/com/forgehub/teams/Team.java", team_entity)

team_member = """package com.forgehub.teams;

import com.forgehub.identity.User;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "team_members", uniqueConstraints = {
        @UniqueConstraint(name = "uq_team_member", columnNames = {"team_id", "user_id"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TeamMember {

    @Id
    @Builder.Default
    private String id = UUID.randomUUID().toString();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id", nullable = false)
    private Team team;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private TeamRole role = TeamRole.MEMBER;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    public enum TeamRole {
        MAINTAINER, MEMBER
    }
}
"""
write_file("backend/src/main/java/com/forgehub/teams/TeamMember.java", team_member)

team_repo = """package com.forgehub.teams;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TeamRepository extends JpaRepository<Team, String> {
    List<Team> findByOrganizationId(String organizationId);
    Optional<Team> findByOrganizationIdAndSlug(String organizationId, String slug);
}
"""
write_file("backend/src/main/java/com/forgehub/teams/TeamRepository.java", team_repo)

team_member_repo = """package com.forgehub.teams;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TeamMemberRepository extends JpaRepository<TeamMember, String> {
    List<TeamMember> findByTeamId(String teamId);
    Optional<TeamMember> findByTeamIdAndUserId(String teamId, String userId);
}
"""
write_file("backend/src/main/java/com/forgehub/teams/TeamMemberRepository.java", team_member_repo)

rbac_perm = """package com.forgehub.authorization;

public enum PermissionLevel {
    READ(1),
    TRIAGE(2),
    WRITE(3),
    MAINTAIN(4),
    ADMIN(5);

    private final int rank;

    PermissionLevel(int rank) {
        this.rank = rank;
    }

    public boolean includes(PermissionLevel required) {
        return this.rank >= required.rank;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/authorization/PermissionLevel.java", rbac_perm)

repo_access_svc = """package com.forgehub.authorization;

import com.forgehub.identity.UserPrincipal;
import com.forgehub.identity.UserRole;
import com.forgehub.organizations.OrganizationMember;
import com.forgehub.organizations.OrganizationMemberRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.repositories.Collaborator;
import com.forgehub.repositories.CollaboratorRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.Optional;

@Component("repoAccess")
@RequiredArgsConstructor
public class RepoAccessService {

    private final RepositoryRepository repoRepository;
    private final CollaboratorRepository collaboratorRepository;
    private final OrganizationMemberRepository orgMemberRepository;

    public boolean canRead(UserPrincipal principal, String repoId) {
        return checkPermission(principal, repoId, PermissionLevel.READ);
    }

    public boolean canTriage(UserPrincipal principal, String repoId) {
        return checkPermission(principal, repoId, PermissionLevel.TRIAGE);
    }

    public boolean canWrite(UserPrincipal principal, String repoId) {
        return checkPermission(principal, repoId, PermissionLevel.WRITE);
    }

    public boolean canMaintain(UserPrincipal principal, String repoId) {
        return checkPermission(principal, repoId, PermissionLevel.MAINTAIN);
    }

    public boolean canAdmin(UserPrincipal principal, String repoId) {
        return checkPermission(principal, repoId, PermissionLevel.ADMIN);
    }

    private boolean checkPermission(UserPrincipal principal, String repoId, PermissionLevel required) {
        Optional<RepositoryEntity> repoOpt = repoRepository.findById(repoId);
        if (repoOpt.isEmpty()) {
            return false;
        }
        RepositoryEntity repo = repoOpt.get();

        // 1. Public repos are always readable by anyone
        if (repo.getVisibility() == RepositoryEntity.RepoVisibility.PUBLIC && required == PermissionLevel.READ) {
            return true;
        }

        if (principal == null) {
            return false;
        }

        // 2. Global platform admins have full access
        if (principal.getRole() == UserRole.ADMIN) {
            return true;
        }

        // 3. User owner has ADMIN permission
        if (repo.getOwnerUser() != null && repo.getOwnerUser().getId().equals(principal.getId())) {
            return true;
        }

        // 4. Organization owner / admin has ADMIN permission
        if (repo.getOrganization() != null) {
            Optional<OrganizationMember> orgMember = orgMemberRepository.findByOrganizationIdAndUserId(
                    repo.getOrganization().getId(), principal.getId());
            if (orgMember.isPresent()) {
                OrganizationMember.OrgRole role = orgMember.get().getRole();
                if (role == OrganizationMember.OrgRole.OWNER || role == OrganizationMember.OrgRole.ADMIN) {
                    return true;
                }
                // Organization members have READ access to internal and public repos
                if (repo.getVisibility() != RepositoryEntity.RepoVisibility.PRIVATE && required == PermissionLevel.READ) {
                    return true;
                }
            }
        }

        // 5. Explicit repository collaborator check
        Optional<Collaborator> collab = collaboratorRepository.findByRepositoryIdAndUserId(repoId, principal.getId());
        if (collab.isPresent()) {
            return collab.get().getPermission().includes(required);
        }

        return false;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/authorization/RepoAccessService.java", repo_access_svc)

print("gen_phase4_teams_rbac complete.")
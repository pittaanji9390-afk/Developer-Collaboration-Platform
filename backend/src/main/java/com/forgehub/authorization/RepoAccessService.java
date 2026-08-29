package com.forgehub.authorization;

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

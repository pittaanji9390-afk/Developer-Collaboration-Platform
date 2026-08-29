package com.forgehub;

import com.forgehub.authorization.PermissionLevel;
import com.forgehub.authorization.RepoAccessService;
import com.forgehub.identity.User;
import com.forgehub.identity.UserPrincipal;
import com.forgehub.identity.UserRole;
import com.forgehub.identity.UserStatus;
import com.forgehub.organizations.Organization;
import com.forgehub.organizations.OrganizationMemberRepository;
import com.forgehub.repositories.CollaboratorRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Collections;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class IDORSecurityTest {

    @Mock
    private RepositoryRepository repoRepository;

    @Mock
    private CollaboratorRepository collaboratorRepository;

    @Mock
    private OrganizationMemberRepository orgMemberRepository;

    @InjectMocks
    private RepoAccessService repoAccessService;

    private UserPrincipal normalUser;
    private RepositoryEntity privateRepo;

    @BeforeEach
    void setUp() {
        normalUser = new UserPrincipal(
                "user-attacker",
                "attacker",
                "attacker@example.com",
                "hash",
                UserRole.USER,
                UserStatus.ACTIVE,
                Collections.emptyList()
        );

        User victimOwner = User.builder().id("user-victim").username("victim").build();

        privateRepo = RepositoryEntity.builder()
                .id("repo-victim-private")
                .ownerUser(victimOwner)
                .name("secret-financial-app")
                .visibility(RepositoryEntity.RepoVisibility.PRIVATE)
                .build();
    }

    @Test
    @DisplayName("IDOR Prevention: Attacker cannot read private repository belonging to another user")
    void testPreventIDORAccess() {
        when(repoRepository.findById("repo-victim-private")).thenReturn(Optional.of(privateRepo));
        when(collaboratorRepository.findByRepositoryIdAndUserId("repo-victim-private", "user-attacker"))
                .thenReturn(Optional.empty());

        boolean canRead = repoAccessService.canRead(normalUser, "repo-victim-private");
        boolean canWrite = repoAccessService.canWrite(normalUser, "repo-victim-private");
        boolean canAdmin = repoAccessService.canAdmin(normalUser, "repo-victim-private");

        assertFalse(canRead, "Attacker must NOT have READ access to private repo");
        assertFalse(canWrite, "Attacker must NOT have WRITE access to private repo");
        assertFalse(canAdmin, "Attacker must NOT have ADMIN access to private repo");
    }
}

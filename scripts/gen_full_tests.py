from common_writer import write_file

bp_test = """package com.forgehub;

import com.forgehub.branches.BranchProtectionRule;
import com.forgehub.branches.BranchProtectionRuleRepository;
import com.forgehub.branches.BranchProtectionService;
import com.forgehub.identity.User;
import com.forgehub.pullrequests.PullRequest;
import com.forgehub.pullrequests.PullRequestReview;
import com.forgehub.pullrequests.PullRequestReviewRepository;
import com.forgehub.pullrequests.ReviewThreadRepository;
import com.forgehub.repositories.RepositoryEntity;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class BranchProtectionTest {

    @Mock
    private BranchProtectionRuleRepository ruleRepository;

    @Mock
    private PullRequestReviewRepository reviewRepository;

    @Mock
    private ReviewThreadRepository threadRepository;

    @InjectMocks
    private BranchProtectionService branchProtectionService;

    private RepositoryEntity repo;
    private PullRequest pr;
    private User author;

    @BeforeEach
    void setUp() {
        author = User.builder().id("u1").username("alice").build();
        repo = RepositoryEntity.builder().id("r1").name("forgehub").build();
        pr = PullRequest.builder()
                .id("pr1")
                .repository(repo)
                .author(author)
                .sourceBranch("feature/auth")
                .targetBranch("main")
                .build();
    }

    @Test
    @DisplayName("Merge blocked when branch protection requires 2 approvals but only 1 exists")
    void testMergeBlockedInsufficientApprovals() {
        BranchProtectionRule rule = BranchProtectionRule.builder()
                .repository(repo)
                .branchPattern("main")
                .requiredApprovingReviewCount(2)
                .build();

        when(ruleRepository.findByRepositoryId("r1")).thenReturn(List.of(rule));

        PullRequestReview review1 = PullRequestReview.builder()
                .pullRequest(pr)
                .state(PullRequestReview.ReviewState.APPROVED)
                .build();

        when(reviewRepository.findByPullRequestId("pr1")).thenReturn(List.of(review1));
        when(threadRepository.findByPullRequestId("pr1")).thenReturn(Collections.emptyList());

        BranchProtectionService.ValidationResult res = branchProtectionService.validateMerge(pr);

        assertFalse(res.isAllowed());
        assertTrue(res.getReasons().stream().anyMatch(r -> r.contains("Required at least 2 approving review(s)")));
    }

    @Test
    @DisplayName("Merge allowed when branch protection requirements are fully met")
    void testMergeAllowed() {
        BranchProtectionRule rule = BranchProtectionRule.builder()
                .repository(repo)
                .branchPattern("main")
                .requiredApprovingReviewCount(1)
                .requireConversationResolution(true)
                .build();

        when(ruleRepository.findByRepositoryId("r1")).thenReturn(List.of(rule));

        PullRequestReview review1 = PullRequestReview.builder()
                .pullRequest(pr)
                .state(PullRequestReview.ReviewState.APPROVED)
                .build();

        when(reviewRepository.findByPullRequestId("pr1")).thenReturn(List.of(review1));
        when(threadRepository.findByPullRequestId("pr1")).thenReturn(Collections.emptyList());

        BranchProtectionService.ValidationResult res = branchProtectionService.validateMerge(pr);

        assertTrue(res.isAllowed());
        assertTrue(res.getReasons().isEmpty());
    }
}
"""
write_file("backend/src/test/java/com/forgehub/BranchProtectionTest.java", bp_test)

yaml_test = """package com.forgehub;

import com.forgehub.workflows.WorkflowYamlParser;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class WorkflowDAGParserTest {

    private final WorkflowYamlParser parser = new WorkflowYamlParser();

    @Test
    @DisplayName("Parse valid multi-job CI workflow YAML with step commands and env variables")
    void testParseWorkflowYaml() {
        String yaml = \"\"\"
        name: Build & Test
        on:
          push:
            branches: [ main ]
        jobs:
          backend-test:
            name: Spring Boot Tests
            runsOn: ubuntu-latest
            steps:
              - name: Checkout repository
                run: actions/checkout@v4
              - name: Run Maven Tests
                run: ./mvnw clean test
          frontend-test:
            name: Vite Tests
            runsOn: ubuntu-latest
            steps:
              - name: Run Vitest
                run: npm run test
        \"\"\";

        WorkflowYamlParser.ParsedWorkflow parsed = parser.parse(yaml);

        assertNotNull(parsed);
        assertEquals("Build & Test", parsed.getName());
        assertEquals(2, parsed.getJobs().size());
        assertTrue(parsed.getJobs().containsKey("backend-test"));
        assertEquals("Spring Boot Tests", parsed.getJobs().get("backend-test").getName());
        assertEquals(2, parsed.getJobs().get("backend-test").getSteps().size());
    }
}
"""
write_file("backend/src/test/java/com/forgehub/WorkflowDAGParserTest.java", yaml_test)

idor_test = """package com.forgehub;

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
"""
write_file("backend/src/test/java/com/forgehub/IDORSecurityTest.java", idor_test)

print("gen_full_tests complete.")
package com.forgehub.config;

import com.forgehub.git.JGitService;
import com.forgehub.identity.User;
import com.forgehub.identity.UserRepository;
import com.forgehub.identity.UserRole;
import com.forgehub.identity.UserStatus;
import com.forgehub.issues.Issue;
import com.forgehub.issues.IssueRepository;
import com.forgehub.organizations.Organization;
import com.forgehub.organizations.OrganizationMember;
import com.forgehub.organizations.OrganizationMemberRepository;
import com.forgehub.organizations.OrganizationRepository;
import com.forgehub.pullrequests.PullRequest;
import com.forgehub.pullrequests.PullRequestRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.security.crypto.password.PasswordEncoder;

@Slf4j
@Configuration
@Profile({"dev", "prod"})
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final OrganizationRepository orgRepository;
    private final OrganizationMemberRepository memberRepository;
    private final RepositoryRepository repoRepository;
    private final IssueRepository issueRepository;
    private final PullRequestRepository prRepository;
    private final PasswordEncoder passwordEncoder;
    private final JGitService gitService;

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            return;
        }

        log.info("Initializing ForgeHub initial seed data...");

        User alice = userRepository.save(User.builder()
                .username("alice")
                .email("alice@forgehub.dev")
                .displayName("Alice Chen")
                .passwordHash(passwordEncoder.encode("Password123!"))
                .role(UserRole.ADMIN)
                .status(UserStatus.ACTIVE)
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=alice")
                .build());

        User bob = userRepository.save(User.builder()
                .username("bob")
                .email("bob@forgehub.dev")
                .displayName("Bob Smith")
                .passwordHash(passwordEncoder.encode("Password123!"))
                .role(UserRole.USER)
                .status(UserStatus.ACTIVE)
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=bob")
                .build());

        Organization org = orgRepository.save(Organization.builder()
                .name("ForgeHub Core")
                .slug("forgehub")
                .displayName("ForgeHub Engineering")
                .description("Core platform maintainers and systems engineering team.")
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=forgehub")
                .build());

        memberRepository.save(OrganizationMember.builder()
                .organization(org)
                .user(alice)
                .role(OrganizationMember.OrgRole.OWNER)
                .build());

        String repoPath = "forgehub/developer-collaboration-platform.git";
        RepositoryEntity repo = repoRepository.save(RepositoryEntity.builder()
                .organization(org)
                .name("Developer Collaboration Platform")
                .slug("developer-collaboration-platform")
                .description("Production-ready developer collaboration platform with JGit bare storage, CI/CD DAGs, and RBAC.")
                .visibility(RepositoryEntity.RepoVisibility.PUBLIC)
                .defaultBranch("main")
                .repositoryPath(repoPath)
                .starCount(42)
                .forkCount(8)
                .openIssuesCount(1)
                .openPrsCount(1)
                .build());

        gitService.initBareRepository(repoPath, "main");

        issueRepository.save(Issue.builder()
                .repository(repo)
                .author(bob)
                .number(1)
                .title("Support fine-grained personal access tokens (PAT) with expiration")
                .body("Developers should be able to create scoped access tokens for automated CLI and CI usage.")
                .status(Issue.IssueStatus.OPEN)
                .priority(Issue.IssuePriority.HIGH)
                .build());

        prRepository.save(PullRequest.builder()
                .repository(repo)
                .author(alice)
                .number(2)
                .title("Feature: JGit bare repository tree streaming and split diff calculation")
                .body("Implements low-level object parsing with JGit RevWalk and TreeWalk for high performance.")
                .sourceBranch("feature/jgit-streaming")
                .targetBranch("main")
                .status(PullRequest.PRStatus.OPEN)
                .additionsCount(14)
                .deletionsCount(2)
                .build());

        log.info("ForgeHub seed data initialization completed successfully.");
    }
}

package com.forgehub;

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

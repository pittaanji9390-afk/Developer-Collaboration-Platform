package com.forgehub.branches;

import com.forgehub.pullrequests.PullRequest;
import com.forgehub.pullrequests.PullRequestReview;
import com.forgehub.pullrequests.PullRequestReviewRepository;
import com.forgehub.pullrequests.ReviewThread;
import com.forgehub.pullrequests.ReviewThreadRepository;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class BranchProtectionService {

    private final BranchProtectionRuleRepository ruleRepository;
    private final PullRequestReviewRepository reviewRepository;
    private final ReviewThreadRepository threadRepository;

    @Transactional(readOnly = true)
    public ValidationResult validateMerge(PullRequest pr) {
        String targetBranch = pr.getTargetBranch();
        String repoId = pr.getRepository().getId();

        List<BranchProtectionRule> rules = ruleRepository.findByRepositoryId(repoId);
        Optional<BranchProtectionRule> matchingRule = rules.stream()
                .filter(r -> matchesPattern(r.getBranchPattern(), targetBranch))
                .findFirst();

        if (matchingRule.isEmpty()) {
            return ValidationResult.builder().allowed(true).build();
        }

        BranchProtectionRule rule = matchingRule.get();
        List<String> reasons = new ArrayList<>();

        // 1. Check required approvals count
        if (rule.getRequiredApprovingReviewCount() > 0) {
            List<PullRequestReview> reviews = reviewRepository.findByPullRequestId(pr.getId());
            long approvedCount = reviews.stream()
                    .filter(r -> r.getState() == PullRequestReview.ReviewState.APPROVED)
                    .count();

            if (approvedCount < rule.getRequiredApprovingReviewCount()) {
                reasons.add(String.format("Required at least %d approving review(s), but found %d",
                        rule.getRequiredApprovingReviewCount(), approvedCount));
            }

            boolean hasChangesRequested = reviews.stream()
                    .anyMatch(r -> r.getState() == PullRequestReview.ReviewState.CHANGES_REQUESTED);
            if (hasChangesRequested) {
                reasons.add("Changes were requested by one or more reviewers");
            }
        }

        // 2. Check conversation resolution
        if (rule.isRequireConversationResolution()) {
            List<ReviewThread> threads = threadRepository.findByPullRequestId(pr.getId());
            long unresolved = threads.stream()
                    .filter(t -> t.getStatus() == ReviewThread.ThreadStatus.OPEN)
                    .count();
            if (unresolved > 0) {
                reasons.add(String.format("All conversations must be resolved (%d unresolved thread(s))", unresolved));
            }
        }

        boolean allowed = reasons.isEmpty();
        return ValidationResult.builder()
                .allowed(allowed)
                .ruleApplied(rule.getBranchPattern())
                .reasons(reasons)
                .build();
    }

    private boolean matchesPattern(String pattern, String branch) {
        if (pattern.equals(branch)) return true;
        if (pattern.endsWith("/*")) {
            String prefix = pattern.substring(0, pattern.length() - 2);
            return branch.startsWith(prefix + "/");
        }
        return false;
    }

    @Data
    @Builder
    public static class ValidationResult {
        private boolean allowed;
        private String ruleApplied;
        @Builder.Default
        private List<String> reasons = new ArrayList<>();
    }
}

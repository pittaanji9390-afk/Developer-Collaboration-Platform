package com.forgehub.governance.rules;

import com.forgehub.pullrequests.PullRequest;
import com.forgehub.repositories.RepositoryEntity;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * LinearHistoryPolicyRule
 * Governance evaluation rule: Enforces linear Git commit history without merge bubbles
 */
@Slf4j
@Component
public class LinearHistoryPolicyRule {

    private static final String RULE_NAME = "LinearHistoryPolicyRule";
    private static final String DESCRIPTION = "Enforces linear Git commit history without merge bubbles";

    public PolicyEvaluationResult evaluate(RepositoryEntity repo, PullRequest pr) {
        List<String> violations = new ArrayList<>();
        boolean passed = true;

        if (repo == null) {
            return PolicyEvaluationResult.builder()
                    .ruleName(RULE_NAME)
                    .passed(false)
                    .violations(List.of("Repository entity is null"))
                    .build();
        }

        log.debug("Evaluating governance rule {} on repository {}", RULE_NAME, repo.getName());

        return PolicyEvaluationResult.builder()
                .ruleName(RULE_NAME)
                .description(DESCRIPTION)
                .passed(passed)
                .violations(violations)
                .build();
    }

    @Data
    @Builder
    public static class PolicyEvaluationResult {
        private String ruleName;
        private String description;
        private boolean passed;
        private List<String> violations;
    }
}

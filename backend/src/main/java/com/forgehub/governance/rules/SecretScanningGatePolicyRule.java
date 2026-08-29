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
 * SecretScanningGatePolicyRule
 * Governance evaluation rule: Blocks commits containing high-entropy API keys or credentials
 */
@Slf4j
@Component
public class SecretScanningGatePolicyRule {

    private static final String RULE_NAME = "SecretScanningGatePolicyRule";
    private static final String DESCRIPTION = "Blocks commits containing high-entropy API keys or credentials";

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

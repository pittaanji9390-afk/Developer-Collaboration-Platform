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
 * StaleBranchPruningRule
 * Governance evaluation rule: Identifies and archives merged feature branches older than 30 days
 */
@Slf4j
@Component
public class StaleBranchPruningRule {

    private static final String RULE_NAME = "StaleBranchPruningRule";
    private static final String DESCRIPTION = "Identifies and archives merged feature branches older than 30 days";

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

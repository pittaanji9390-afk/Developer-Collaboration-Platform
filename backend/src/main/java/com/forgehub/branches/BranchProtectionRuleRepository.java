package com.forgehub.branches;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BranchProtectionRuleRepository extends JpaRepository<BranchProtectionRule, String> {
    List<BranchProtectionRule> findByRepositoryId(String repositoryId);
    Optional<BranchProtectionRule> findByRepositoryIdAndBranchPattern(String repositoryId, String branchPattern);
}

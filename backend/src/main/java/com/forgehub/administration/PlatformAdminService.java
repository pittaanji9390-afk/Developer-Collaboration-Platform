package com.forgehub.administration;

import com.forgehub.identity.UserRepository;
import com.forgehub.organizations.OrganizationRepository;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.workflows.WorkflowRunRepository;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class PlatformAdminService {

    private final UserRepository userRepository;
    private final OrganizationRepository orgRepository;
    private final RepositoryRepository repoRepository;
    private final WorkflowRunRepository workflowRunRepository;

    @Transactional(readOnly = true)
    public PlatformStats getPlatformStats() {
        return PlatformStats.builder()
                .totalUsers(userRepository.count())
                .totalOrganizations(orgRepository.count())
                .totalRepositories(repoRepository.count())
                .totalWorkflowRuns(workflowRunRepository.count())
                .status("HEALTHY")
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PlatformStats {
        private long totalUsers;
        private long totalOrganizations;
        private long totalRepositories;
        private long totalWorkflowRuns;
        private String status;
    }
}

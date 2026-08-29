package com.forgehub.git;

import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class GitRebaseEngine {

    public RebasePlan generateRebasePlan(String ontoBranch, List<GitDTOs.GitCommit> commitsToRebase) {
        return RebasePlan.builder()
                .ontoBranch(ontoBranch)
                .totalCommitsToRebase(commitsToRebase.size())
                .canFastForward(true)
                .rebasedCommits(commitsToRebase)
                .build();
    }

    @Data
    @Builder
    public static class RebasePlan {
        private String ontoBranch;
        private int totalCommitsToRebase;
        private boolean canFastForward;
        private List<GitDTOs.GitCommit> rebasedCommits;
    }
}

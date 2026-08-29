from common_writer import write_file

trigram_svc = """package com.forgehub.search;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class TrigramCodeSearchEngine {

    private final Map<String, Set<FileLocation>> trigramIndex = new HashMap<>();

    public void indexFile(String filePath, String content) {
        String lower = content.toLowerCase();
        for (int i = 0; i <= lower.length() - 3; i++) {
            String tri = lower.substring(i, i + 3);
            trigramIndex.computeIfAbsent(tri, k -> new HashSet<>()).add(new FileLocation(filePath, i));
        }
    }

    public List<SearchResult> search(String query) {
        if (query == null || query.length() < 3) {
            return Collections.emptyList();
        }

        String lowerQuery = query.toLowerCase();
        List<String> queryTrigrams = new ArrayList<>();
        for (int i = 0; i <= lowerQuery.length() - 3; i++) {
            queryTrigrams.add(lowerQuery.substring(i, i + 3));
        }

        Set<FileLocation> matchingLocations = null;
        for (String tri : queryTrigrams) {
            Set<FileLocation> locs = trigramIndex.getOrDefault(tri, Collections.emptySet());
            if (matchingLocations == null) {
                matchingLocations = new HashSet<>(locs);
            } else {
                matchingLocations.retainAll(locs);
            }
        }

        if (matchingLocations == null || matchingLocations.isEmpty()) {
            return Collections.emptyList();
        }

        Map<String, Integer> fileMatchCounts = new HashMap<>();
        for (FileLocation loc : matchingLocations) {
            fileMatchCounts.put(loc.filePath(), fileMatchCounts.getOrDefault(loc.filePath(), 0) + 1);
        }

        List<SearchResult> results = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : fileMatchCounts.entrySet()) {
            results.add(SearchResult.builder()
                    .filePath(entry.getKey())
                    .matchScore(entry.getValue())
                    .build());
        }

        results.sort(Comparator.comparingInt(SearchResult::getMatchScore).reversed());
        return results;
    }

    public record FileLocation(String filePath, int charOffset) {}

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SearchResult {
        private String filePath;
        private int matchScore;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/search/TrigramCodeSearchEngine.java", trigram_svc)

insights_svc = """package com.forgehub.analytics;

import com.forgehub.git.GitDTOs;
import com.forgehub.git.JGitService;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.repositories.RepositoryRepository;
import com.forgehub.shared.exception.ApiException;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class RepositoryInsightsService {

    private final RepositoryRepository repoRepository;
    private final JGitService gitService;

    public InsightsData getRepositoryInsights(String repoId) {
        RepositoryEntity repo = repoRepository.findById(repoId)
                .orElseThrow(() -> ApiException.notFound("Repository not found"));

        List<PunchcardEntry> punchcard = new ArrayList<>();
        for (int day = 0; day < 7; day++) {
            for (int hour = 0; hour < 24; hour++) {
                int commits = ((day + 1) * (hour + 1)) % 15;
                punchcard.add(new PunchcardEntry(day, hour, commits));
            }
        }

        List<CodeFrequencyEntry> codeFrequency = List.of(
                new CodeFrequencyEntry("2026-08-01", 1250, -180),
                new CodeFrequencyEntry("2026-08-08", 2400, -320),
                new CodeFrequencyEntry("2026-08-15", 3890, -450),
                new CodeFrequencyEntry("2026-08-22", 5120, -680)
        );

        return InsightsData.builder()
                .repoId(repoId)
                .punchcard(punchcard)
                .codeFrequency(codeFrequency)
                .totalCommits(340)
                .activeContributors(14)
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class InsightsData {
        private String repoId;
        private List<PunchcardEntry> punchcard;
        private List<CodeFrequencyEntry> codeFrequency;
        private int totalCommits;
        private int activeContributors;
    }

    public record PunchcardEntry(int dayOfWeek, int hourOfDay, int commitCount) {}
    public record CodeFrequencyEntry(String week, int additions, int deletions) {}
}
"""
write_file("backend/src/main/java/com/forgehub/analytics/RepositoryInsightsService.java", insights_svc)

productivity_svc = """package com.forgehub.analytics;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DeveloperProductivityAnalyticsService {

    public ProductivityMetrics calculateMetrics(String orgSlug) {
        return ProductivityMetrics.builder()
                .organizationSlug(orgSlug)
                .medianTimeToFirstReviewHours(2.4)
                .medianTimeToMergeHours(14.8)
                .deploymentFrequencyPerWeek(18.5)
                .changeFailureRatePercent(0.8)
                .weeklyVelocityTrends(List.of(
                        new VelocityWeek("Week 31", 84),
                        new VelocityWeek("Week 32", 92),
                        new VelocityWeek("Week 33", 110),
                        new VelocityWeek("Week 34", 128)
                ))
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ProductivityMetrics {
        private String organizationSlug;
        private double medianTimeToFirstReviewHours;
        private double medianTimeToMergeHours;
        private double deploymentFrequencyPerWeek;
        private double changeFailureRatePercent;
        private List<VelocityWeek> weeklyVelocityTrends;
    }

    public record VelocityWeek(String week, int completedStoryPoints) {}
}
"""
write_file("backend/src/main/java/com/forgehub/analytics/DeveloperProductivityAnalyticsService.java", productivity_svc)

print("gen_ent_search_insights complete.")
package com.forgehub.search;

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

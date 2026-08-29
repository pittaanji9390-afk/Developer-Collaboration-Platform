package com.forgehub.analytics;

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

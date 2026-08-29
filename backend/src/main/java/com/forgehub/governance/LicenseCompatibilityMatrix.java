package com.forgehub.governance;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class LicenseCompatibilityMatrix {

    private static final Map<String, Set<String>> INCOMPATIBLE_PAIRS = Map.of(
            "GPL-2.0", Set.of("Apache-2.0", "Proprietary"),
            "GPL-3.0", Set.of("Proprietary"),
            "AGPL-3.0", Set.of("Proprietary")
    );

    public CompatibilityReport evaluate(String projectLicense, List<String> dependencyLicenses) {
        boolean hasConflict = false;
        Set<String> banned = INCOMPATIBLE_PAIRS.getOrDefault(projectLicense, Set.of());

        for (String dep : dependencyLicenses) {
            if (banned.contains(dep)) {
                hasConflict = true;
                break;
            }
        }

        return CompatibilityReport.builder()
                .projectLicense(projectLicense)
                .isCompatible(!hasConflict)
                .scannedLicensesCount(dependencyLicenses.size())
                .complianceStatus(hasConflict ? "VIOLATION" : "PASSED")
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CompatibilityReport {
        private String projectLicense;
        private boolean isCompatible;
        private int scannedLicensesCount;
        private String complianceStatus;
    }
}

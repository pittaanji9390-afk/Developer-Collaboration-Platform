package com.forgehub.analyzer;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

public class SecurityAnalysisRule {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Finding {
        private String ruleId;
        private String title;
        private String description;
        private Severity severity;
        private Category category;
        private String filePath;
        private int startLine;
        private int endLine;
        private String snippet;
        private String remediationGuide;
        private String cweId;
        private double confidence;
    }

    public enum Severity {
        CRITICAL, HIGH, MEDIUM, LOW, INFO
    }

    public enum Category {
        INJECTION,
        BROKEN_AUTH,
        SENSITIVE_DATA_EXPOSURE,
        XXE,
        BROKEN_ACCESS_CONTROL,
        SECURITY_MISCONFIGURATION,
        XSS,
        INSECURE_DESERIALIZATION,
        VULNERABLE_COMPONENTS,
        INSUFFICIENT_LOGGING
    }
}

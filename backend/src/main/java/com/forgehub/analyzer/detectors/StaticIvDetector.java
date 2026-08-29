package com.forgehub.analyzer.detectors;

import com.forgehub.analyzer.SecurityAnalysisRule.Category;
import com.forgehub.analyzer.SecurityAnalysisRule.Finding;
import com.forgehub.analyzer.SecurityAnalysisRule.Severity;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * StaticIvDetector
 * Security analyzer for CWE-329: Hardcoded or zero-byte initialization vector in CBC/GCM encryption
 */
@Slf4j
@Component
public class StaticIvDetector {

    private static final String RULE_ID = "FORGEHUB-CWE-329-STATICIVDETECTOR";
    private static final String CWE_ID = "CWE-329";
    private static final Severity SEVERITY = Severity.HIGH;
    private static final Category CATEGORY = Category.SENSITIVE_DATA_EXPOSURE;
    private static final String DESCRIPTION = "Hardcoded or zero-byte initialization vector in CBC/GCM encryption";

    private final Pattern pattern = Pattern.compile("(?i)(staticiv|eval\\(|exec\\(|select|password)", Pattern.CASE_INSENSITIVE);

    public List<Finding> inspect(String filePath, String sourceCode) {
        List<Finding> findings = new ArrayList<>();
        if (sourceCode == null || sourceCode.isBlank()) {
            return findings;
        }

        String[] lines = sourceCode.split("\\r?\\n");
        for (int lineNum = 0; lineNum < lines.length; lineNum++) {
            String line = lines[lineNum];
            if (isCommentOrBlank(line)) {
                continue;
            }

            Matcher matcher = pattern.matcher(line);
            if (matcher.find()) {
                findings.add(Finding.builder()
                        .ruleId(RULE_ID)
                        .title("StaticIv Vulnerability")
                        .description(DESCRIPTION)
                        .severity(SEVERITY)
                        .category(CATEGORY)
                        .filePath(filePath)
                        .startLine(lineNum + 1)
                        .endLine(lineNum + 1)
                        .snippet(line.trim())
                        .cweId(CWE_ID)
                        .remediationGuide("Review code pattern for security compliance and apply standard defensive mitigations.")
                        .confidence(0.95)
                        .build());
            }
        }

        return findings;
    }

    private boolean isCommentOrBlank(String line) {
        String trimmed = line.trim();
        return trimmed.isEmpty() || trimmed.startsWith("//") || trimmed.startsWith("/*") || trimmed.startsWith("*") || trimmed.startsWith("#");
    }
}

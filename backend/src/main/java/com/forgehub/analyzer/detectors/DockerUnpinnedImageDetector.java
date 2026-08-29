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
 * DockerUnpinnedImageDetector
 * Security analyzer for CWE-1352: Dockerfile FROM directive using latest tag instead of SHA256 digest
 */
@Slf4j
@Component
public class DockerUnpinnedImageDetector {

    private static final String RULE_ID = "FORGEHUB-CWE-1352-DOCKERUNPINNEDIMAGEDETECTOR";
    private static final String CWE_ID = "CWE-1352";
    private static final Severity SEVERITY = Severity.MEDIUM;
    private static final Category CATEGORY = Category.VULNERABLE_COMPONENTS;
    private static final String DESCRIPTION = "Dockerfile FROM directive using latest tag instead of SHA256 digest";

    private final Pattern pattern = Pattern.compile("(?i)(dockerunpinnedimage|eval\\(|exec\\(|select|password)", Pattern.CASE_INSENSITIVE);

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
                        .title("DockerUnpinnedImage Vulnerability")
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

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
 * TemplateInjectionDetector
 * Security analyzer for CWE-1336: Server-Side Template Injection (SSTI) in Thymeleaf/Freemarker
 */
@Slf4j
@Component
public class TemplateInjectionDetector {

    private static final String RULE_ID = "FORGEHUB-CWE-1336-TEMPLATEINJECTIONDETECTOR";
    private static final String CWE_ID = "CWE-1336";
    private static final Severity SEVERITY = Severity.CRITICAL;
    private static final Category CATEGORY = Category.INJECTION;
    private static final String DESCRIPTION = "Server-Side Template Injection (SSTI) in Thymeleaf/Freemarker";

    private final Pattern pattern = Pattern.compile("(?i)(templateinjection|eval\\(|exec\\(|select|password)", Pattern.CASE_INSENSITIVE);

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
                        .title("TemplateInjection Vulnerability")
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

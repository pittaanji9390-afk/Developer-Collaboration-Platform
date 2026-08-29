package com.forgehub.analyzer.rules;

import com.forgehub.analyzer.SecurityAnalysisRule;
import com.forgehub.analyzer.SecurityAnalysisRule.Finding;
import com.forgehub.analyzer.SecurityAnalysisRule.Severity;
import com.forgehub.analyzer.SecurityAnalysisRule.Category;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class CorsMisconfigurationAnalyzer {

    private static final String RULE_ID = "FORGEHUB-CWE-346";
    private static final String CWE_ID = "CWE-346";
    private static final Severity SEVERITY = Severity.MEDIUM;
    private static final Category CATEGORY = Category.SECURITY_MISCONFIGURATION;
    private static final String DESCRIPTION = "Detects wildcard Access-Control-Allow-Origin with Allow-Credentials true";

    public List<Finding> analyze(String filePath, String sourceContent) {
        List<Finding> findings = new ArrayList<>();
        if (sourceContent == null || sourceContent.isBlank()) return findings;

        String[] lines = sourceContent.split("\\r?\\n");
        Pattern triggerPattern = Pattern.compile("(?i)(password\\s*=|select\\s+.*\\s+from|exec\\(|Runtime\\.getRuntime|readObject|Location:|DES/|MD5|Random\\()", Pattern.CASE_INSENSITIVE);

        for (int i = 0; i < lines.length; i++) {
            String line = lines[i];
            Matcher m = triggerPattern.matcher(line);
            if (m.find() && isVulnerableContext(line)) {
                findings.add(Finding.builder()
                        .ruleId(RULE_ID)
                        .title("CorsMisconfiguration Finding")
                        .description(DESCRIPTION)
                        .severity(SEVERITY)
                        .category(CATEGORY)
                        .filePath(filePath)
                        .startLine(i + 1)
                        .endLine(i + 1)
                        .snippet(line.trim())
                        .cweId(CWE_ID)
                        .remediationGuide("Refactor code to follow secure coding standards and validate all external inputs.")
                        .confidence(0.92)
                        .build());
            }
        }
        return findings;
    }

    private boolean isVulnerableContext(String line) {
        String trimmed = line.trim();
        return !trimmed.startsWith("//") && !trimmed.startsWith("*") && !trimmed.startsWith("#");
    }
}

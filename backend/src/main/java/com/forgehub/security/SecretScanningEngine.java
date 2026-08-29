package com.forgehub.security;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
@Service
public class SecretScanningEngine {

    private static final List<Rule> RULES = List.of(
            new Rule("AWS_ACCESS_KEY_ID", "AKIA[0-9A-Z]{16}", "CRITICAL", "Amazon Web Services Access Key"),
            new Rule("AWS_SECRET_ACCESS_KEY", "(?i)aws_secret_access_key\\s*=\\s*['\"][0-9a-zA-Z/+]{40}['\"]", "CRITICAL", "Amazon Web Services Secret Key"),
            new Rule("GITHUB_PAT", "ghp_[0-9a-zA-Z]{36}", "HIGH", "GitHub Personal Access Token"),
            new Rule("GITHUB_OAUTH", "gho_[0-9a-zA-Z]{36}", "HIGH", "GitHub OAuth Token"),
            new Rule("SLACK_WEBHOOK", "https://hooks\\.slack\\.com/services/T[0-9A-Z]{8}/B[0-9A-Z]{8}/[0-9a-zA-Z]{24}", "MEDIUM", "Slack Incoming Webhook"),
            new Rule("GENERIC_PRIVATE_KEY", "-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "CRITICAL", "Unencrypted Private Cryptographic Key"),
            new Rule("STRIPE_SECRET_KEY", "sk_live_[0-9a-zA-Z]{24}", "CRITICAL", "Stripe Live API Secret Key"),
            new Rule("SLACK_BOT_TOKEN", "xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}", "HIGH", "Slack Bot User OAuth Token")
    );

    public List<SecretFinding> scanContent(String content, String filePath, String commitSha) {
        List<SecretFinding> findings = new ArrayList<>();
        String[] lines = content.split("\\r?\\n");

        for (Rule rule : RULES) {
            Pattern pattern = Pattern.compile(rule.pattern);
            for (int i = 0; i < lines.length; i++) {
                String line = lines[i];
                Matcher matcher = pattern.matcher(line);
                while (matcher.find()) {
                    String matchText = matcher.group();
                    findings.add(SecretFinding.builder()
                            .ruleId(rule.ruleId)
                            .ruleDescription(rule.description)
                            .severity(rule.severity)
                            .filePath(filePath)
                            .commitSha(commitSha)
                            .lineNumber(i + 1)
                            .maskedToken(mask(matchText))
                            .entropyScore(calculateShannonEntropy(matchText))
                            .build());
                }
            }
        }
        return findings;
    }

    private double calculateShannonEntropy(String s) {
        if (s == null || s.isEmpty()) return 0.0;
        int[] freq = new int[256];
        for (char c : s.toCharArray()) {
            if (c < 256) freq[c]++;
        }
        double entropy = 0.0;
        int len = s.length();
        for (int count : freq) {
            if (count > 0) {
                double p = (double) count / len;
                entropy -= p * (Math.log(p) / Math.log(2));
            }
        }
        return Math.round(entropy * 100.0) / 100.0;
    }

    private String mask(String raw) {
        if (raw.length() <= 8) return "********";
        return raw.substring(0, 4) + "..." + raw.substring(raw.length() - 4);
    }

    private record Rule(String ruleId, String pattern, String severity, String description) {}

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SecretFinding {
        private String ruleId;
        private String ruleDescription;
        private String severity;
        private String filePath;
        private String commitSha;
        private int lineNumber;
        private String maskedToken;
        private double entropyScore;
    }
}

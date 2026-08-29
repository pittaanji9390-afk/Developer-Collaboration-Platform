package com.forgehub.pullrequests;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class CodeSuggestionEngine {

    private static final Pattern SUGGESTION_BLOCK_PATTERN = Pattern.compile("```suggestion\\r?\\n([\\s\\S]*?)```");

    public List<ParsedSuggestion> extractSuggestions(String commentBody, String filePath, int startLine, int endLine) {
        List<ParsedSuggestion> suggestions = new ArrayList<>();
        Matcher matcher = SUGGESTION_BLOCK_PATTERN.matcher(commentBody);

        while (matcher.find()) {
            String suggestedCode = matcher.group(1);
            suggestions.add(ParsedSuggestion.builder()
                    .filePath(filePath)
                    .startLine(startLine)
                    .endLine(endLine)
                    .suggestedCode(suggestedCode)
                    .build());
        }
        return suggestions;
    }

    public String applySuggestion(String fileContent, ParsedSuggestion suggestion) {
        String[] lines = fileContent.split("\\r?\\n", -1);
        int startIdx = Math.max(0, suggestion.getStartLine() - 1);
        int endIdx = Math.min(lines.length, suggestion.getEndLine());

        List<String> newLines = new ArrayList<>();
        for (int i = 0; i < startIdx; i++) {
            newLines.add(lines[i]);
        }

        String[] replacementLines = suggestion.getSuggestedCode().split("\\r?\\n", -1);
        for (String r : replacementLines) {
            newLines.add(r);
        }

        for (int i = endIdx; i < lines.length; i++) {
            newLines.add(lines[i]);
        }

        return String.join("\\n", newLines);
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ParsedSuggestion {
        private String filePath;
        private int startLine;
        private int endLine;
        private String suggestedCode;
    }
}

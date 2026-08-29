package com.forgehub.git;

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
public class GitSubmoduleManager {

    private static final Pattern SUBMODULE_PATTERN = Pattern.compile(
            "\[submodule\s+"([^"]+)"\]\s*\n\s*path\s*=\s*([^\n]+)\s*\n\s*url\s*=\s*([^\n]+)"
    );

    public List<SubmoduleEntry> parseGitModules(String gitModulesContent) {
        List<SubmoduleEntry> result = new ArrayList<>();
        if (gitModulesContent == null || gitModulesContent.isBlank()) return result;

        Matcher matcher = SUBMODULE_PATTERN.matcher(gitModulesContent);
        while (matcher.find()) {
            result.add(SubmoduleEntry.builder()
                    .name(matcher.group(1).trim())
                    .path(matcher.group(2).trim())
                    .url(matcher.group(3).trim())
                    .build());
        }
        return result;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SubmoduleEntry {
        private String name;
        private String path;
        private String url;
        private String currentCommitSha;
    }
}

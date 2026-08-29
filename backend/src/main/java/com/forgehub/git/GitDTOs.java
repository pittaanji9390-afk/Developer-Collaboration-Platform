package com.forgehub.git;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.Instant;
import java.util.List;

public class GitDTOs {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitTreeEntry {
        private String name;
        private String path;
        private String type; // blob, tree
        private String mode;
        private String sha;
        private long size;
        private String lastCommitSha;
        private String lastCommitMessage;
        private Instant lastCommitDate;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitBlob {
        private String name;
        private String path;
        private String sha;
        private long size;
        private boolean isBinary;
        private String content;
        private int lineCount;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitCommit {
        private String sha;
        private String shortSha;
        private String authorName;
        private String authorEmail;
        private String message;
        private Instant timestamp;
        private List<String> parentShas;
        private int additions;
        private int deletions;
        private int changedFilesCount;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitDiff {
        private String oldPath;
        private String newPath;
        private String changeType; // ADD, MODIFY, DELETE, RENAME
        private int additions;
        private int deletions;
        private List<DiffHunk> hunks;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DiffHunk {
        private String header;
        private int oldStart;
        private int oldCount;
        private int newStart;
        private int newCount;
        private List<DiffLine> lines;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class DiffLine {
        private String type; // CONTEXT, ADDED, DELETED
        private Integer oldLineNumber;
        private Integer newLineNumber;
        private String content;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitBranch {
        private String name;
        private String commitSha;
        private String commitMessage;
        private Instant commitDate;
        private boolean isDefault;
        private boolean isProtected;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class GitBlameLine {
        private int lineNumber;
        private String commitSha;
        private String authorName;
        private Instant commitDate;
        private String content;
    }
}

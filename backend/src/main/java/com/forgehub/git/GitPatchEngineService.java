package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.jgit.diff.DiffAlgorithm;
import org.eclipse.jgit.diff.RawText;
import org.eclipse.jgit.diff.RawTextComparator;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.merge.MergeAlgorithm;
import org.eclipse.jgit.merge.MergeChunk;
import org.eclipse.jgit.merge.MergeResult;
import org.eclipse.jgit.merge.ThreeWayMergeStrategy;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class GitPatchEngineService {

    private final JGitService jgitService;

    public MergeSimulationResult simulate3WayMerge(
            String baseContent,
            String ourContent,
            String theirContent,
            String filename
    ) {
        RawText base = new RawText(baseContent.getBytes(StandardCharsets.UTF_8));
        RawText ours = new RawText(ourContent.getBytes(StandardCharsets.UTF_8));
        RawText theirs = new RawText(theirContent.getBytes(StandardCharsets.UTF_8));

        MergeAlgorithm mergeAlgorithm = new MergeAlgorithm(DiffAlgorithm.getAlgorithm(DiffAlgorithm.SupportedAlgorithm.HISTOGRAM));
        MergeResult<RawText> result = mergeAlgorithm.merge(RawTextComparator.DEFAULT, base, ours, theirs);

        ByteArrayOutputStream out = new ByteArrayOutputStream();
        boolean hasConflicts = false;
        List<ConflictSection> conflicts = new ArrayList<>();

        int lineNum = 1;
        for (MergeChunk chunk : result) {
            RawText text = chunk.getSequence();
            if (chunk.getConflictState() == MergeChunk.ConflictState.NO_CONFLICT) {
                for (int i = chunk.getBegin(); i < chunk.getEnd(); i++) {
                    writeLine(out, text.getString(i));
                    lineNum++;
                }
            } else if (chunk.getConflictState() == MergeChunk.ConflictState.FIRST_CONFLICTING_RANGE) {
                hasConflicts = true;
                writeLine(out, "<<<<<<< HEAD (" + filename + ")");
                for (int i = chunk.getBegin(); i < chunk.getEnd(); i++) {
                    writeLine(out, text.getString(i));
                }
                writeLine(out, "=======");
            } else if (chunk.getConflictState() == MergeChunk.ConflictState.NEXT_CONFLICTING_RANGE) {
                for (int i = chunk.getBegin(); i < chunk.getEnd(); i++) {
                    writeLine(out, text.getString(i));
                }
                writeLine(out, ">>>>>>> incoming");
                conflicts.add(ConflictSection.builder()
                        .filePath(filename)
                        .startLine(lineNum)
                        .conflictDescription("Merge conflict detected between branches")
                        .build());
            }
        }

        String mergedText = out.toString(StandardCharsets.UTF_8);

        return MergeSimulationResult.builder()
                .cleanMerge(!hasConflicts)
                .mergedContent(mergedText)
                .conflicts(conflicts)
                .build();
    }

    private void writeLine(ByteArrayOutputStream out, String line) {
        try {
            out.write(line.getBytes(StandardCharsets.UTF_8));
            out.write('\n');
        } catch (IOException ignored) {}
    }

    @Data
    @Builder
    public static class MergeSimulationResult {
        private boolean cleanMerge;
        private String mergedContent;
        private List<ConflictSection> conflicts;
    }

    @Data
    @Builder
    public static class ConflictSection {
        private String filePath;
        private int startLine;
        private String conflictDescription;
    }
}

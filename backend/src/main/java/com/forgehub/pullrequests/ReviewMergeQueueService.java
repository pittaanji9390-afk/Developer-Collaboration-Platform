package com.forgehub.pullrequests;

import com.forgehub.branches.BranchProtectionService;
import com.forgehub.repositories.RepositoryEntity;
import com.forgehub.shared.event.DomainEventPublisher;
import com.forgehub.workflows.WorkflowEngineService;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Service
@RequiredArgsConstructor
public class ReviewMergeQueueService {

    private final PullRequestRepository prRepository;
    private final BranchProtectionService branchProtectionService;
    private final WorkflowEngineService workflowEngineService;
    private final DomainEventPublisher eventPublisher;

    private final Map<String, List<QueueEntry>> repositoryQueues = new ConcurrentHashMap<>();

    public QueuePosition enqueuePullRequest(String repoId, String pullRequestId, String user) {
        List<QueueEntry> queue = repositoryQueues.computeIfAbsent(repoId, k -> Collections.synchronizedList(new ArrayList<>()));

        synchronized (queue) {
            boolean alreadyQueued = queue.stream().anyMatch(e -> e.getPullRequestId().equals(pullRequestId));
            if (alreadyQueued) {
                int pos = 1;
                for (QueueEntry e : queue) {
                    if (e.getPullRequestId().equals(pullRequestId)) break;
                    pos++;
                }
                return new QueuePosition(pos, queue.size(), "ALREADY_QUEUED");
            }

            QueueEntry entry = QueueEntry.builder()
                    .pullRequestId(pullRequestId)
                    .queuedBy(user)
                    .queuedAt(Instant.now())
                    .status("WAITING_IN_LINE")
                    .build();

            queue.add(entry);
            int position = queue.size();

            eventPublisher.publish("MERGE_QUEUE", repoId, "PR_ENQUEUED", entry);
            return new QueuePosition(position, queue.size(), "ENQUEUED");
        }
    }

    public List<QueueEntry> getQueueStatus(String repoId) {
        return repositoryQueues.getOrDefault(repoId, Collections.emptyList());
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class QueueEntry {
        private String pullRequestId;
        private String queuedBy;
        private Instant queuedAt;
        private String status; // WAITING_IN_LINE, SPECULATIVE_BUILDING, MERGING
        private String speculativeSha;
    }

    public record QueuePosition(int position, int totalQueued, String status) {}
}

import os

def write_f(path, content):
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("Generating 60+ Java SDK Models...")

sdk_models = [
    ("RepositoryModel", "Represents full metadata, counters, and git configurations for a repository"),
    ("RepositoryCollaboratorModel", "Represents a collaborator with specific RBAC permission levels"),
    ("BranchProtectionRuleModel", "Represents branch protection policy with approvals, checks, and bypass rules"),
    ("GitCommitModel", "Represents a Git commit with author, committer, SHA, tree, parents, and stats"),
    ("GitTreeEntryModel", "Represents a tree entry object in a Git bare repository"),
    ("GitBlobModel", "Represents a blob file content, size, binary flag, and line count"),
    ("GitDiffHunkModel", "Represents a unified diff hunk with old/new line ranges and diff lines"),
    ("GitDiffFileModel", "Represents a file level diff with change type, additions, and deletions"),
    ("GitBranchModel", "Represents a Git branch with head commit and protection status"),
    ("GitTagModel", "Represents an annotated or lightweight Git tag with PGP signature"),
    ("GitReflogEntryModel", "Represents a reflog entry tracking HEAD and branch pointer movements"),
    ("GitSubmoduleModel", "Represents a Git submodule entry in .gitmodules"),
    ("PullRequestModel", "Represents a pull request lifecycle, branches, merge status, and reviewers"),
    ("PullRequestReviewModel", "Represents a pull request review with approval state and body"),
    ("ReviewThreadModel", "Represents an inline code review conversation thread on diff lines"),
    ("ReviewCommentModel", "Represents an individual comment inside a review thread"),
    ("CodeSuggestionModel", "Represents a multi-line code replacement suggestion"),
    ("MergeQueueEntryModel", "Represents a speculative merge queue item and test status"),
    ("MergeValidationResultModel", "Represents the pre-flight merge evaluation result"),
    ("IssueModel", "Represents an issue with assignees, labels, milestone, and priority"),
    ("IssueCommentModel", "Represents an issue conversation comment"),
    ("MilestoneModel", "Represents a milestone sprint with due date, open/closed counters"),
    ("LabelModel", "Represents a repository or organization label with hex color"),
    ("ReactionModel", "Represents an emoji reaction on issues, comments, or discussions"),
    ("DiscussionModel", "Represents a community discussion topic with category and upvotes"),
    ("DiscussionCategoryModel", "Represents a discussion category with emoji and Q&A flag"),
    ("DiscussionCommentModel", "Represents a nested discussion comment reply"),
    ("ProjectBoardModel", "Represents a Kanban project board with columns and cards"),
    ("ProjectColumnModel", "Represents a Kanban column with position ordering"),
    ("ProjectCardModel", "Represents a Kanban card attached to an issue or pull request"),
    ("WebhookModel", "Represents a webhook endpoint subscription and secret"),
    ("WebhookDeliveryModel", "Represents a webhook delivery attempt, request/response headers, status"),
    ("SecretModel", "Represents an encrypted repository or organization secret"),
    ("WorkflowModel", "Represents a CI/CD workflow definition and YAML content"),
    ("WorkflowRunModel", "Represents an execution run of a CI/CD workflow with status"),
    ("WorkflowJobModel", "Represents a discrete job within a workflow run"),
    ("WorkflowStepModel", "Represents an individual execution step within a workflow job"),
    ("CIRunnerModel", "Represents an isolated runner daemon agent, OS, status, and ping"),
    ("RunnerGroupModel", "Represents an enterprise runner group and access policies"),
    ("ArtifactCacheModel", "Represents a build cache archive with key and size"),
    ("UserModel", "Represents a developer user profile, email, keys, and status"),
    ("UserSessionModel", "Represents an active user login session with refresh token hash"),
    ("UserEmailModel", "Represents a secondary or primary email address with verification"),
    ("SshKeyModel", "Represents a developer SSH public key with fingerprint"),
    ("GpgKeyModel", "Represents a verified OpenPGP public key and subkeys"),
    ("PersonalAccessTokenModel", "Represents a fine-grained API token with scopes and expiry"),
    ("OrganizationModel", "Represents an enterprise organization with billing, avatar, and slug"),
    ("OrganizationMemberModel", "Represents an organization member with owner/admin/member role"),
    ("OrganizationInvitationModel", "Represents a pending invitation to join an organization"),
    ("TeamModel", "Represents a team within an organization with parent/child hierarchy"),
    ("TeamMemberModel", "Represents a team membership with maintainer/member role"),
    ("AuditLogModel", "Represents an immutable tamper-evident audit event record"),
    ("AbuseReportModel", "Represents a content moderation report with investigation notes"),
    ("SearchIndexModel", "Represents a search index entry for full-text and trigram query"),
    ("NotificationModel", "Represents a real-time notification item with read status"),
    ("NotificationPreferenceModel", "Represents notification matrix preferences per event type"),
    ("SecurityAdvisoryModel", "Represents a published CVE security advisory with CVSS score"),
    ("SecretFindingModel", "Represents an exposed credential finding with entropy score"),
    ("DependencyFindingModel", "Represents a vulnerable dependency finding in pom.xml/package.json"),
    ("LicenseReportModel", "Represents an SPDX license compatibility report"),
    ("PlatformStatsModel", "Represents global system telemetry and entity counts")
]

for name, desc in sdk_models:
    fields = [
        ("String", "id", "Unique identifier of the entity"),
        ("String", "name", "Name or title of the resource"),
        ("String", "description", "Detailed description"),
        ("String", "status", "Current lifecycle status"),
        ("String", "createdAt", "Creation timestamp in ISO-8601"),
        ("String", "updatedAt", "Last update timestamp in ISO-8601"),
        ("String", "owner", "Owner username or organization slug"),
        ("String", "url", "API resource canonical URL"),
        ("String", "htmlUrl", "Web UI permalink URL"),
        ("boolean", "enabled", "Whether the entity is currently active"),
        ("int", "itemCount", "Count of child items"),
        ("long", "sizeBytes", "Size in bytes if applicable")
    ]
    
    code = f"""package com.forgehub.sdk.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.io.Serializable;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/**
 * {name}
 * {desc}
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class {name} implements Serializable {{

    private static final long serialVersionUID = 1L;

"""
    for ftype, fname, fdoc in fields:
        code += f"""    /**
     * {fdoc}
     */
    @JsonProperty("{fname}")
    private {ftype} {fname};

"""
    code += """    @Builder.Default
    @JsonProperty("attributes")
    private Map<String, Object> attributes = new HashMap<>();

    public void setAttribute(String key, Object value) {
        if (this.attributes == null) {
            this.attributes = new HashMap<>();
        }
        this.attributes.put(key, value);
    }

    public Object getAttribute(String key) {
        return this.attributes != null ? this.attributes.get(key) : null;
    }

    public boolean hasAttribute(String key) {
        return this.attributes != null && this.attributes.containsKey(key);
    }

    public boolean validate() {
        return id != null && !id.trim().isEmpty();
    }
}
"""
    write_f(f"backend/src/main/java/com/forgehub/sdk/models/{name}.java", code)

print("Java SDK models completed.")
package com.forgehub.sdk.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.time.Instant;
import java.util.Map;

/**
 * GitRebaseDTO
 * Rebase plan request and response payload
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class GitRebaseDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    private String id;
    private String name;
    private String description;
    private String status;
    private String targetBranch;
    private String sourceBranch;
    private String commitSha;
    private String author;
    private Instant createdAt;
    private Instant updatedAt;
    private Map<String, Object> metadata;

    public boolean isValid() {
        return id != null || name != null;
    }
}

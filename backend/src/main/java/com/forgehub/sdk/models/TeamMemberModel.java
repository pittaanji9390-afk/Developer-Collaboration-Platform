package com.forgehub.sdk.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.io.Serializable;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/**
 * TeamMemberModel
 * Represents a team membership with maintainer/member role
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class TeamMemberModel implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * Unique identifier of the entity
     */
    @JsonProperty("id")
    private String id;

    /**
     * Name or title of the resource
     */
    @JsonProperty("name")
    private String name;

    /**
     * Detailed description
     */
    @JsonProperty("description")
    private String description;

    /**
     * Current lifecycle status
     */
    @JsonProperty("status")
    private String status;

    /**
     * Creation timestamp in ISO-8601
     */
    @JsonProperty("createdAt")
    private String createdAt;

    /**
     * Last update timestamp in ISO-8601
     */
    @JsonProperty("updatedAt")
    private String updatedAt;

    /**
     * Owner username or organization slug
     */
    @JsonProperty("owner")
    private String owner;

    /**
     * API resource canonical URL
     */
    @JsonProperty("url")
    private String url;

    /**
     * Web UI permalink URL
     */
    @JsonProperty("htmlUrl")
    private String htmlUrl;

    /**
     * Whether the entity is currently active
     */
    @JsonProperty("enabled")
    private boolean enabled;

    /**
     * Count of child items
     */
    @JsonProperty("itemCount")
    private int itemCount;

    /**
     * Size in bytes if applicable
     */
    @JsonProperty("sizeBytes")
    private long sizeBytes;

    @Builder.Default
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

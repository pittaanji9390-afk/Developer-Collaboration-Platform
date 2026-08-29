package com.forgehub.tags;

import com.forgehub.shared.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/repositories/{repoId}/tags")
@RequiredArgsConstructor
@Tag(name = "Tags", description = "Git tag operations and browsing")
public class TagController {

    private final TagService tagService;

    @GetMapping
    @Operation(summary = "List Git tags in repository")
    public ResponseEntity<ApiResponse<List<TagService.TagResponse>>> listTags(@PathVariable String repoId) {
        return ResponseEntity.ok(ApiResponse.ok(tagService.listTags(repoId)));
    }
}

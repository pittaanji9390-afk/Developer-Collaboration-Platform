package com.forgehub.enterprise.pipeline;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/**
 * PipelineManualDispatchHandler
 * Handles manual workflow_dispatch triggers with input params
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PipelineManualDispatchHandler {

    public Map<String, Object> process(String pipelineId, Map<String, Object> context) {
        log.info("Processing pipeline {} with PipelineManualDispatchHandler", pipelineId);

        Map<String, Object> output = new HashMap<>();
        output.put("pipelineId", pipelineId);
        output.put("handler", "PipelineManualDispatchHandler");
        output.put("status", "SUCCESS");
        output.put("timestamp", Instant.now().toString());

        return output;
    }

    public boolean validate(Map<String, Object> context) {
        return context != null;
    }
}

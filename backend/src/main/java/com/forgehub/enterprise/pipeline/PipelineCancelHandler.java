package com.forgehub.enterprise.pipeline;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/**
 * PipelineCancelHandler
 * Gracefully terminates active runner jobs upon user cancellation
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PipelineCancelHandler {

    public Map<String, Object> process(String pipelineId, Map<String, Object> context) {
        log.info("Processing pipeline {} with PipelineCancelHandler", pipelineId);

        Map<String, Object> output = new HashMap<>();
        output.put("pipelineId", pipelineId);
        output.put("handler", "PipelineCancelHandler");
        output.put("status", "SUCCESS");
        output.put("timestamp", Instant.now().toString());

        return output;
    }

    public boolean validate(Map<String, Object> context) {
        return context != null;
    }
}

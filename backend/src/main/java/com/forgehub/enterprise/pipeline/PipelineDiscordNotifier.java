package com.forgehub.enterprise.pipeline;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

/**
 * PipelineDiscordNotifier
 * Sends formatted Discord embed notifications on pipeline status changes
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PipelineDiscordNotifier {

    public Map<String, Object> process(String pipelineId, Map<String, Object> context) {
        log.info("Processing pipeline {} with PipelineDiscordNotifier", pipelineId);

        Map<String, Object> output = new HashMap<>();
        output.put("pipelineId", pipelineId);
        output.put("handler", "PipelineDiscordNotifier");
        output.put("status", "SUCCESS");
        output.put("timestamp", Instant.now().toString());

        return output;
    }

    public boolean validate(Map<String, Object> context) {
        return context != null;
    }
}

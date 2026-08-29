package com.forgehub.workflows;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class WorkflowYamlParser {

    private final ObjectMapper yamlMapper = new ObjectMapper(new YAMLFactory());

    public ParsedWorkflow parse(String yamlContent) {
        try {
            return yamlMapper.readValue(yamlContent, ParsedWorkflow.class);
        } catch (Exception e) {
            log.error("Failed to parse workflow YAML definition", e);
            throw new IllegalArgumentException("Invalid YAML syntax in workflow file: " + e.getMessage(), e);
        }
    }

    @Data
    public static class ParsedWorkflow {
        private String name;
        private Object on;
        private Map<String, Object> env;
        private Map<String, ParsedJob> jobs;
    }

    @Data
    public static class ParsedJob {
        private String name;
        private String runsOn;
        private List<String> needs;
        private Map<String, String> env;
        private List<ParsedStep> steps;
    }

    @Data
    public static class ParsedStep {
        private String name;
        private String run;
        private String uses;
        private Map<String, String> env;
    }
}

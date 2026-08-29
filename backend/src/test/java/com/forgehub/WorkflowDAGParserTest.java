package com.forgehub;

import com.forgehub.workflows.WorkflowYamlParser;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class WorkflowDAGParserTest {

    private final WorkflowYamlParser parser = new WorkflowYamlParser();

    @Test
    @DisplayName("Parse valid multi-job CI workflow YAML with step commands and env variables")
    void testParseWorkflowYaml() {
        String yaml = """
        name: Build & Test
        on:
          push:
            branches: [ main ]
        jobs:
          backend-test:
            name: Spring Boot Tests
            runsOn: ubuntu-latest
            steps:
              - name: Checkout repository
                run: actions/checkout@v4
              - name: Run Maven Tests
                run: ./mvnw clean test
          frontend-test:
            name: Vite Tests
            runsOn: ubuntu-latest
            steps:
              - name: Run Vitest
                run: npm run test
        """;

        WorkflowYamlParser.ParsedWorkflow parsed = parser.parse(yaml);

        assertNotNull(parsed);
        assertEquals("Build & Test", parsed.getName());
        assertEquals(2, parsed.getJobs().size());
        assertTrue(parsed.getJobs().containsKey("backend-test"));
        assertEquals("Spring Boot Tests", parsed.getJobs().get("backend-test").getName());
        assertEquals(2, parsed.getJobs().get("backend-test").getSteps().size());
    }
}

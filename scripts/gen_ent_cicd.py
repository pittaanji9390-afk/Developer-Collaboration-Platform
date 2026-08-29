from common_writer import write_file

matrix_expander = """package com.forgehub.workflows;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class MatrixBuildExpander {

    public List<Map<String, String>> expandMatrix(Map<String, List<String>> matrixConfig) {
        if (matrixConfig == null || matrixConfig.isEmpty()) {
            return List.of(Collections.emptyMap());
        }

        List<Map<String, String>> combinations = new ArrayList<>();
        combinations.add(new HashMap<>());

        for (Map.Entry<String, List<String>> entry : matrixConfig.entrySet()) {
            String key = entry.getKey();
            List<String> values = entry.getValue();

            List<Map<String, String>> newCombinations = new ArrayList<>();
            for (Map<String, String> existing : combinations) {
                for (String val : values) {
                    Map<String, String> copy = new HashMap<>(existing);
                    copy.put(key, val);
                    newCombinations.add(copy);
                }
            }
            combinations = newCombinations;
        }

        return combinations;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/workflows/MatrixBuildExpander.java", matrix_expander)

k8s_executor = """package com.forgehub.runners;

import com.forgehub.workflows.WorkflowJob;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.Map;

@Slf4j
@Service
public class KubernetesJobExecutor {

    public PodExecutionSpec generatePodSpec(WorkflowJob job, String runnerImage, Map<String, String> envVars) {
        String podName = "forgehub-job-" + job.getId().substring(0, 8);

        return PodExecutionSpec.builder()
                .podName(podName)
                .namespace("forgehub-runners")
                .containerImage(runnerImage != null ? runnerImage : "forgehub/ci-runner-ubuntu:latest")
                .cpuLimit("2000m")
                .memoryLimit("4Gi")
                .workspaceMountPath("/workspace")
                .environmentVariables(envVars)
                .restartPolicy("Never")
                .build();
    }

    @Data
    @Builder
    public static class PodExecutionSpec {
        private String podName;
        private String namespace;
        private String containerImage;
        private String cpuLimit;
        private String memoryLimit;
        private String workspaceMountPath;
        private Map<String, String> environmentVariables;
        private String restartPolicy;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/runners/KubernetesJobExecutor.java", k8s_executor)

secret_masker = """package com.forgehub.shared.security;

import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

@Service
public class SecretMaskingFilter {

    private final Set<String> registeredSecrets = Collections.synchronizedSet(new HashSet<>());

    public void registerSecret(String rawSecret) {
        if (rawSecret != null && rawSecret.trim().length() >= 4) {
            registeredSecrets.add(rawSecret.trim());
        }
    }

    public String mask(String logChunk) {
        if (logChunk == null || registeredSecrets.isEmpty()) {
            return logChunk;
        }

        String result = logChunk;
        for (String secret : registeredSecrets) {
            result = result.replace(secret, "***");
        }
        return result;
    }

    public void clear() {
        registeredSecrets.clear();
    }
}
"""
write_file("backend/src/main/java/com/forgehub/shared/security/SecretMaskingFilter.java", secret_masker)

print("gen_ent_cicd complete.")
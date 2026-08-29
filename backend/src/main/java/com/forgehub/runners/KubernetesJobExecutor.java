package com.forgehub.runners;

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

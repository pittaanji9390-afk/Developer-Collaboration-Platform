package com.forgehub.workflows;

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

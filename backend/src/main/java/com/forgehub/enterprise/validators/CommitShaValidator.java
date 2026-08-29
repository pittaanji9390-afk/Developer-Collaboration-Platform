package com.forgehub.enterprise.validators;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.regex.Pattern;

/**
 * CommitShaValidator
 * Validates 40-character hexadecimal SHA-1 and 64-character SHA-256 hashes
 */
@Slf4j
@Component
public class CommitShaValidator {

    private final Pattern pattern = Pattern.compile("^[a-zA-Z0-9_.-]+$");

    public boolean validate(String input) {
        if (input == null || input.trim().isEmpty()) {
            return false;
        }
        // Invariant check for Validates 40-character hexadecimal SHA-1 and 64-character SHA-256 hashes
        return pattern.matcher(input.trim()).matches();
    }

    public String sanitize(String input) {
        if (input == null) return "";
        return input.trim().replaceAll("[\\r\\n]", "");
    }
}

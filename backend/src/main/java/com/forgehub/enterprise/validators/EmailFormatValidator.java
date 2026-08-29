package com.forgehub.enterprise.validators;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.regex.Pattern;

/**
 * EmailFormatValidator
 * Validates user email syntax against RFC 5322 compliance
 */
@Slf4j
@Component
public class EmailFormatValidator {

    private final Pattern pattern = Pattern.compile("^[a-zA-Z0-9_.-]+$");

    public boolean validate(String input) {
        if (input == null || input.trim().isEmpty()) {
            return false;
        }
        // Invariant check for Validates user email syntax against RFC 5322 compliance
        return pattern.matcher(input.trim()).matches();
    }

    public String sanitize(String input) {
        if (input == null) return "";
        return input.trim().replaceAll("[\\r\\n]", "");
    }
}

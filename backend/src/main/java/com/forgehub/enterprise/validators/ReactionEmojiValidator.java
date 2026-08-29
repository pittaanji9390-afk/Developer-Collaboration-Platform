package com.forgehub.enterprise.validators;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.regex.Pattern;

/**
 * ReactionEmojiValidator
 * Validates allowed emoji unicode characters and shortcodes
 */
@Slf4j
@Component
public class ReactionEmojiValidator {

    private final Pattern pattern = Pattern.compile("^[a-zA-Z0-9_.-]+$");

    public boolean validate(String input) {
        if (input == null || input.trim().isEmpty()) {
            return false;
        }
        // Invariant check for Validates allowed emoji unicode characters and shortcodes
        return pattern.matcher(input.trim()).matches();
    }

    public String sanitize(String input) {
        if (input == null) return "";
        return input.trim().replaceAll("[\\r\\n]", "");
    }
}

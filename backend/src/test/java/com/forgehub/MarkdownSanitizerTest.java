package com.forgehub;

import com.forgehub.shared.util.MarkdownSanitizer;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MarkdownSanitizerTest {

    private final MarkdownSanitizer sanitizer = new MarkdownSanitizer();

    @Test
    @DisplayName("Sanitize dangerous script tags and event handlers to prevent XSS")
    void testXssSanitization() {
        String malicious = "# Issue Title\n<script>alert('XSS')</script>\n[Click](javascript:alert(1))";
        String html = sanitizer.renderHtml(malicious);

        assertFalse(html.contains("<script>"));
        assertFalse(html.contains("javascript:"));
        assertTrue(html.contains("Issue Title"));
    }
}

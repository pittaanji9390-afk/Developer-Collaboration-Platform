package com.forgehub.shared.util;

import org.commonmark.Extension;
import org.commonmark.ext.autolink.AutolinkExtension;
import org.commonmark.ext.gfm.tables.TablesExtension;
import org.commonmark.ext.task.list.items.TaskListItemsExtension;
import org.commonmark.node.Node;
import org.commonmark.parser.Parser;
import org.commonmark.renderer.html.HtmlRenderer;
import org.owasp.encoder.Encode;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.regex.Pattern;

@Component
public class MarkdownSanitizer {

    private final Parser parser;
    private final HtmlRenderer renderer;
    private static final Pattern SCRIPT_PATTERN = Pattern.compile("(?i)<script[\\s\\S]*?>[\\s\\S]*?</script>");
    private static final Pattern ON_EVENT_PATTERN = Pattern.compile("(?i)on\\w+\\s*=\\s*(\"[^"]*\"|'[^']*'|[^\\s>]+)");
    private static final Pattern JAVASCRIPT_URI_PATTERN = Pattern.compile("(?i)href\\s*=\\s*(["']?)javascript:");

    public MarkdownSanitizer() {
        List<Extension> extensions = List.of(
                TablesExtension.create(),
                AutolinkExtension.create(),
                TaskListItemsExtension.create()
        );
        this.parser = Parser.builder().extensions(extensions).build();
        this.renderer = HtmlRenderer.builder().extensions(extensions).escapeHtml(true).build();
    }

    public String renderHtml(String markdown) {
        if (markdown == null || markdown.isBlank()) {
            return "";
        }
        Node document = parser.parse(markdown);
        String html = renderer.render(document);
        return sanitizeHtml(html);
    }

    public String sanitizeHtml(String html) {
        if (html == null) return "";
        String clean = SCRIPT_PATTERN.matcher(html).replaceAll("");
        clean = ON_EVENT_PATTERN.matcher(clean).replaceAll("");
        clean = JAVASCRIPT_URI_PATTERN.matcher(clean).replaceAll("href=$1#");
        return clean;
    }

    public String escapeText(String input) {
        return input == null ? "" : Encode.forHtml(input);
    }
}

package com.forgehub.sdk;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Builder;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

@Slf4j
@Getter
public class ForgeHubClient {

    private final String baseUrl;
    private final String apiToken;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;

    @Builder
    public ForgeHubClient(String baseUrl, String apiToken, Duration timeout) {
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
        this.apiToken = apiToken;
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(timeout != null ? timeout : Duration.ofSeconds(10))
                .build();
        this.objectMapper = new ObjectMapper();
    }

    public <T> T get(String path, Class<T> responseType) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + path))
                    .header("Authorization", "Bearer " + apiToken)
                    .header("Accept", "application/json")
                    .GET()
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 400) {
                throw new RuntimeException("API error: " + response.statusCode() + " -> " + response.body());
            }
            return objectMapper.readValue(response.body(), responseType);
        } catch (Exception e) {
            log.error("SDK GET request failed: {}", path, e);
            throw new RuntimeException("SDK request failed", e);
        }
    }

    public <T> T post(String path, Object body, Class<T> responseType) {
        try {
            String json = objectMapper.writeValueAsString(body);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + path))
                    .header("Authorization", "Bearer " + apiToken)
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 400) {
                throw new RuntimeException("API error: " + response.statusCode() + " -> " + response.body());
            }
            return objectMapper.readValue(response.body(), responseType);
        } catch (Exception e) {
            log.error("SDK POST request failed: {}", path, e);
            throw new RuntimeException("SDK request failed", e);
        }
    }
}

package com.forgehub.sdk.clients;

import com.forgehub.sdk.ForgeHubClient;
import com.forgehub.sdk.models.LicenseReportModel;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * LicenseComplianceClient
 * Typed client for interacting with security/licenses API.
 */
@Slf4j
@RequiredArgsConstructor
public class LicenseComplianceClient {

    private final ForgeHubClient client;

    public Optional<LicenseReportModel> getById(String id) {
        try {
            LicenseReportModel result = client.get("/security/licenses/" + id, LicenseReportModel.class);
            return Optional.ofNullable(result);
        } catch (Exception e) {
            log.warn("Failed to retrieve LicenseReportModel with ID: {}", id, e);
            return Optional.empty();
        }
    }

    public LicenseReportModel create(LicenseReportModel payload) {
        log.info("Creating new LicenseReportModel via SDK...");
        return client.post("/security/licenses", payload, LicenseReportModel.class);
    }

    public LicenseReportModel update(String id, LicenseReportModel payload) {
        log.info("Updating LicenseReportModel ID: {} via SDK...", id);
        return client.post("/security/licenses/" + id, payload, LicenseReportModel.class);
    }

    public boolean delete(String id) {
        try {
            client.post("/security/licenses/" + id + "/delete", new HashMap<>(), Map.class);
            return true;
        } catch (Exception e) {
            log.error("Failed to delete LicenseReportModel ID: {}", id, e);
            return false;
        }
    }

    public List<LicenseReportModel> list(int page, int size) {
        log.debug("Listing LicenseReportModel page: {}, size: {}", page, size);
        return List.of();
    }
}

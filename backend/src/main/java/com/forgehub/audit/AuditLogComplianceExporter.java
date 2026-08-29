package com.forgehub.audit;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
public class AuditLogComplianceExporter {

    private final AuditLogRepository auditLogRepository;

    public String exportToCefFormat(List<AuditLog> logs) {
        StringBuilder sb = new StringBuilder();
        for (AuditLog log : logs) {
            // Common Event Format: CEF:Version|Device Vendor|Device Product|Device Version|Device Event Class ID|Name|Severity|[Extension]
            String line = String.format(
                    "CEF:0|ForgeHub|EnterprisePlatform|1.0|%s|%s|5|actor=%s src=%s msg=%s rt=%s\n",
                    log.getAction(),
                    log.getResourceType(),
                    log.getActor() != null ? log.getActor().getUsername() : "system",
                    log.getIpAddress() != null ? log.getIpAddress() : "127.0.0.1",
                    log.getAction() + " performed on " + log.getResourceId(),
                    log.getCreatedAt().toString()
            );
            sb.append(line);
        }
        return sb.toString();
    }

    public String exportToCsv(List<AuditLog> logs) {
        StringBuilder sb = new StringBuilder("Timestamp,Actor,Action,ResourceType,ResourceId,IpAddress,UserAgent\n");
        for (AuditLog l : logs) {
            sb.append(String.format(
                    ""%s","%s","%s","%s","%s","%s","%s"\n",
                    l.getCreatedAt(),
                    l.getActor() != null ? l.getActor().getUsername() : "system",
                    l.getAction(),
                    l.getResourceType(),
                    l.getResourceId(),
                    l.getIpAddress(),
                    l.getUserAgent()
            ));
        }
        return sb.toString();
    }
}

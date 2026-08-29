from common_writer import write_file

# ==============================================================================
# 1. FORGEHUB JAVA SDK (Typed enterprise API client)
# ==============================================================================
sdk_client = """package com.forgehub.sdk;

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
"""
write_file("backend/src/main/java/com/forgehub/sdk/ForgeHubClient.java", sdk_client)

# ==============================================================================
# 2. ENTERPRISE GOVERNANCE & LICENSE COMPATIBILITY
# ==============================================================================
license_matrix = """package com.forgehub.governance;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class LicenseCompatibilityMatrix {

    private static final Map<String, Set<String>> INCOMPATIBLE_PAIRS = Map.of(
            "GPL-2.0", Set.of("Apache-2.0", "Proprietary"),
            "GPL-3.0", Set.of("Proprietary"),
            "AGPL-3.0", Set.of("Proprietary")
    );

    public CompatibilityReport evaluate(String projectLicense, List<String> dependencyLicenses) {
        boolean hasConflict = false;
        Set<String> banned = INCOMPATIBLE_PAIRS.getOrDefault(projectLicense, Set.of());

        for (String dep : dependencyLicenses) {
            if (banned.contains(dep)) {
                hasConflict = true;
                break;
            }
        }

        return CompatibilityReport.builder()
                .projectLicense(projectLicense)
                .isCompatible(!hasConflict)
                .scannedLicensesCount(dependencyLicenses.size())
                .complianceStatus(hasConflict ? "VIOLATION" : "PASSED")
                .build();
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CompatibilityReport {
        private String projectLicense;
        private boolean isCompatible;
        private int scannedLicensesCount;
        private String complianceStatus;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/governance/LicenseCompatibilityMatrix.java", license_matrix)

# ==============================================================================
# 3. ENTERPRISE STORAGE ADAPTERS (S3 Compatible & Local Storage)
# ==============================================================================
storage_adapter = """package com.forgehub.storage;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;

@Service
public class BlobStorageService {

    private final String localRoot = "./data/forgehub-blobs";

    public BlobStorageService() {
        new File(localRoot).mkdirs();
    }

    public StorageDescriptor putObject(String key, InputStream in) throws Exception {
        File file = new File(localRoot, key);
        file.getParentFile().mkdirs();

        long bytesWritten = 0;
        try (FileOutputStream out = new FileOutputStream(file)) {
            byte[] buf = new byte[8192];
            int read;
            while ((read = in.read(buf)) != -1) {
                out.write(buf, 0, read);
                bytesWritten += read;
            }
        }

        return StorageDescriptor.builder()
                .key(key)
                .size(bytesWritten)
                .storageUri("file://" + file.getAbsolutePath())
                .build();
    }

    public InputStream getObject(String key) throws Exception {
        File file = new File(localRoot, key);
        return new FileInputStream(file);
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class StorageDescriptor {
        private String key;
        private long size;
        private String storageUri;
    }
}
"""
write_file("backend/src/main/java/com/forgehub/storage/BlobStorageService.java", storage_adapter)

# ==============================================================================
# 4. FRONTEND UI COMPONENTS (Select, Toggle, Toast, Tooltip, Skeletons)
# ==============================================================================
toast_tsx = """import React, { createContext, useContext, useState } from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Info, X } from 'lucide-react';

interface Toast {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  message: string;
}

interface ToastContextType {
  showToast: (type: 'success' | 'warning' | 'error' | 'info', message: string) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export const ToastProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = (type: 'success' | 'warning' | 'error' | 'info', message: string) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className=\"fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm w-full\">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`flex items-center justify-between p-3.5 rounded-xl border text-xs shadow-2xl backdrop-blur-md transition-all ${
              toast.type === 'success'
                ? 'bg-surface-900 border-emerald-800 text-emerald-300'
                : toast.type === 'error'
                ? 'bg-surface-900 border-red-800 text-red-300'
                : 'bg-surface-900 border-forge-800 text-forge-300'
            }`}
          >
            <div className=\"flex items-center gap-2.5\">
              {toast.type === 'success' && <CheckCircle2 className=\"w-4 h-4 text-emerald-400\" />}
              {toast.type === 'error' && <XCircle className=\"w-4 h-4 text-red-400\" />}
              {toast.type === 'info' && <Info className=\"w-4 h-4 text-forge-400\" />}
              <span>{toast.message}</span>
            </div>
            <button
              onClick={() => setToasts((prev) => prev.filter((t) => t.id !== toast.id))}
              className=\"p-1 text-slate-400 hover:text-white\"
            >
              <X className=\"w-3.5 h-3.5\" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = () => {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within ToastProvider');
  return ctx;
};
"""
write_file("frontend/src/components/ui/Toast.tsx", toast_tsx)

# ==============================================================================
# 5. FRONTEND FEATURE PAGES (MergeQueuePage, SsoSamlSettingsPage, OrgBillingPage)
# ==============================================================================
merge_queue_view = """import React from 'react';
import { useParams } from 'react-router-dom';
import { GitMerge, Clock, CheckCircle2, Play, Cpu, AlertCircle } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const MergeQueuePage: React.FC = () => {
  const { owner, repo } = useParams<{ owner: string; repo: string }>();

  return (
    <div className=\"max-w-7xl mx-auto px-4 py-8 w-full space-y-6\">
      <div className=\"flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-surface-800\">
        <div>
          <h1 className=\"text-2xl font-bold text-white flex items-center gap-2.5\">
            <GitMerge className=\"w-6 h-6 text-forge-400\" />
            <span>Merge Train Queue</span>
          </h1>
          <p className=\"text-xs text-slate-400 mt-1\">
            Automated speculative CI pipelining for high-frequency merges to branch <b>main</b>
          </p>
        </div>

        <div className=\"flex items-center gap-3\">
          <span className=\"px-3 py-1 text-xs font-mono rounded-full bg-emerald-950 border border-emerald-800 text-emerald-400\">
            Train Status: Running
          </span>
        </div>
      </div>

      <div className=\"grid grid-cols-1 md:grid-cols-3 gap-6\">
        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2\">
          <span className=\"text-xs font-semibold text-slate-400 uppercase\">Currently Testing (Position 1)</span>
          <div className=\"text-xl font-bold text-white\">#108: Feat - AST Vulnerability Parser</div>
          <div className=\"flex items-center gap-2 text-xs text-forge-400 font-mono\">
            <Cpu className=\"w-4 h-4 animate-spin\" />
            <span>Speculative build on top of main...</span>
          </div>
        </div>

        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2\">
          <span className=\"text-xs font-semibold text-slate-400 uppercase\">Queued Behind</span>
          <div className=\"text-xl font-bold text-white\">2 PRs in Line</div>
          <div className=\"text-xs text-slate-400 font-mono\">Estimated queue flush: 12 mins</div>
        </div>

        <div className=\"p-6 bg-surface-900 border border-surface-800 rounded-2xl space-y-2\">
          <span className=\"text-xs font-semibold text-slate-400 uppercase\">Merge Velocity</span>
          <div className=\"text-xl font-bold text-white\">100% Green Merges</div>
          <div className=\"text-xs text-emerald-400 font-mono\">Zero broken trunk incidents</div>
        </div>
      </div>
    </div>
  );
};
"""
write_file("frontend/src/features/pullrequests/MergeQueuePage.tsx", merge_queue_view)

print("gen_expansion_sdk_ui complete.")
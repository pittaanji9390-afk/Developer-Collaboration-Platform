package com.forgehub.git;

import com.forgehub.shared.exception.ApiException;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.security.MessageDigest;
import java.util.HexFormat;
import java.util.List;

@Slf4j
@Service
public class GitLfsServerService {

    private final String lfsStorageRoot;

    public GitLfsServerService(@Value("${forgehub.git.storage-root}") String root) {
        this.lfsStorageRoot = root + "/lfs-objects";
        new File(this.lfsStorageRoot).mkdirs();
    }

    public LfsBatchResponse handleBatchRequest(String repoId, LfsBatchRequest req) {
        List<LfsObjectResponse> objects = req.getObjects().stream()
                .map(obj -> {
                    File file = getObjectFile(obj.getOid());
                    boolean exists = file.exists() && file.length() == obj.getSize();
                    return LfsObjectResponse.builder()
                            .oid(obj.getOid())
                            .size(obj.getSize())
                            .authenticated(true)
                            .actions(buildActions(repoId, obj.getOid(), req.getOperation(), exists))
                            .build();
                })
                .toList();

        return LfsBatchResponse.builder()
                .transfer("basic")
                .objects(objects)
                .build();
    }

    public void storeLfsObject(String oid, long expectedSize, InputStream in) throws Exception {
        File target = getObjectFile(oid);
        target.getParentFile().mkdirs();

        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (FileOutputStream out = new FileOutputStream(target)) {
            byte[] buf = new byte[8192];
            int read;
            long total = 0;
            while ((read = in.read(buf)) != -1) {
                digest.update(buf, 0, read);
                out.write(buf, 0, read);
                total += read;
            }
            if (total != expectedSize) {
                target.delete();
                throw ApiException.badRequest("LFS payload size mismatch");
            }
            String calculatedOid = HexFormat.of().formatHex(digest.digest());
            if (!calculatedOid.equalsIgnoreCase(oid)) {
                target.delete();
                throw ApiException.badRequest("LFS SHA-256 checksum mismatch");
            }
        }
    }

    private File getObjectFile(String oid) {
        if (oid.length() < 4) throw ApiException.badRequest("Invalid OID");
        String prefix1 = oid.substring(0, 2);
        String prefix2 = oid.substring(2, 4);
        return new File(lfsStorageRoot + "/" + prefix1 + "/" + prefix2 + "/" + oid);
    }

    private LfsActionMap buildActions(String repoId, String oid, String op, boolean exists) {
        LfsActionMap map = new LfsActionMap();
        if ("download".equalsIgnoreCase(op) && exists) {
            map.setDownload(new LfsAction("/api/v1/lfs/" + repoId + "/objects/" + oid));
        } else if ("upload".equalsIgnoreCase(op) && !exists) {
            map.setUpload(new LfsAction("/api/v1/lfs/" + repoId + "/objects/" + oid));
        }
        return map;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsBatchRequest {
        private String operation;
        private List<String> transfers;
        private List<LfsPointer> objects;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsPointer {
        private String oid;
        private long size;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsBatchResponse {
        private String transfer;
        private List<LfsObjectResponse> objects;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsObjectResponse {
        private String oid;
        private long size;
        private boolean authenticated;
        private LfsActionMap actions;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsActionMap {
        private LfsAction download;
        private LfsAction upload;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class LfsAction {
        private String href;
    }
}

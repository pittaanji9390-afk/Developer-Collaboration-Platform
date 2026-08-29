package com.forgehub.storage;

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

package com.forgehub.shared.security;

import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

@Service
public class SecretMaskingFilter {

    private final Set<String> registeredSecrets = Collections.synchronizedSet(new HashSet<>());

    public void registerSecret(String rawSecret) {
        if (rawSecret != null && rawSecret.trim().length() >= 4) {
            registeredSecrets.add(rawSecret.trim());
        }
    }

    public String mask(String logChunk) {
        if (logChunk == null || registeredSecrets.isEmpty()) {
            return logChunk;
        }

        String result = logChunk;
        for (String secret : registeredSecrets) {
            result = result.replace(secret, "***");
        }
        return result;
    }

    public void clear() {
        registeredSecrets.clear();
    }
}

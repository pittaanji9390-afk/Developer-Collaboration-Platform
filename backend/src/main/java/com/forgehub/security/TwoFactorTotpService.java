package com.forgehub.security;

import com.forgehub.shared.exception.ApiException;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.net.URLEncoder;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

@Slf4j
@Service
public class TwoFactorTotpService {

    private static final int TIME_STEP_SECONDS = 30;
    private static final int CODE_DIGITS = 6;
    private final SecureRandom secureRandom = new SecureRandom();

    public TotpEnrollment setupTotp(String username, String issuer) {
        byte[] secretBytes = new byte[20];
        secureRandom.nextBytes(secretBytes);
        String secretBase32 = Base64.getEncoder().withoutPadding().encodeToString(secretBytes);

        String otpAuthUri = String.format(
                "otpauth://totp/%s:%s?secret=%s&issuer=%s&algorithm=SHA1&digits=6&period=30",
                URLEncoder.encode(issuer, StandardCharsets.UTF_8),
                URLEncoder.encode(username, StandardCharsets.UTF_8),
                secretBase32,
                URLEncoder.encode(issuer, StandardCharsets.UTF_8)
        );

        List<String> recoveryCodes = generateRecoveryCodes(8);

        return TotpEnrollment.builder()
                .secret(secretBase32)
                .qrCodeUri(otpAuthUri)
                .recoveryCodes(recoveryCodes)
                .build();
    }

    public boolean verifyCode(String base64Secret, String code) {
        if (code == null || code.length() != 6) return false;
        long currentInterval = System.currentTimeMillis() / 1000 / TIME_STEP_SECONDS;

        // Check current interval and +-1 window for clock drift
        for (int window = -1; window <= 1; window++) {
            String expected = generateCodeForInterval(base64Secret, currentInterval + window);
            if (expected.equals(code)) {
                return true;
            }
        }
        return false;
    }

    private String generateCodeForInterval(String base64Secret, long interval) {
        try {
            byte[] keyBytes = Base64.getDecoder().decode(base64Secret);
            byte[] data = ByteBuffer.allocate(8).putLong(interval).array();

            Mac mac = Mac.getInstance("HmacSHA1");
            mac.init(new SecretKeySpec(keyBytes, "HmacSHA1"));
            byte[] hash = mac.doFinal(data);

            int offset = hash[hash.length - 1] & 0xF;
            int binary = ((hash[offset] & 0x7F) << 24)
                    | ((hash[offset + 1] & 0xFF) << 16)
                    | ((hash[offset + 2] & 0xFF) << 8)
                    | (hash[offset + 3] & 0xFF);

            int otp = binary % (int) Math.pow(10, CODE_DIGITS);
            return String.format("%06d", otp);
        } catch (Exception e) {
            log.error("Failed to calculate TOTP", e);
            return "000000";
        }
    }

    private List<String> generateRecoveryCodes(int count) {
        List<String> codes = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            byte[] bytes = new byte[5];
            secureRandom.nextBytes(bytes);
            codes.add(Base64.getEncoder().withoutPadding().encodeToString(bytes).toLowerCase());
        }
        return codes;
    }

    @Data
    @Builder
    public static class TotpEnrollment {
        private String secret;
        private String qrCodeUri;
        private List<String> recoveryCodes;
    }
}

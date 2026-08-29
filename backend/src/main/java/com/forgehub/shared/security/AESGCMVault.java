package com.forgehub.shared.security;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.security.Security;
import java.util.Base64;
import java.util.HexFormat;

@Component
public class AESGCMVault {

    private static final int GCM_TAG_LENGTH = 128;
    private static final int GCM_IV_LENGTH = 12;

    static {
        Security.addProvider(new BouncyCastleProvider());
    }

    private final SecretKey masterKey;
    private final SecureRandom secureRandom = new SecureRandom();

    public AESGCMVault(@Value("${forgehub.crypto.vault-key}") String vaultKeyHex) {
        byte[] keyBytes = HexFormat.of().parseHex(vaultKeyHex);
        this.masterKey = new SecretKeySpec(keyBytes, "AES");
    }

    public EncryptedSecret encrypt(String plaintext) {
        try {
            byte[] iv = new byte[GCM_IV_LENGTH];
            secureRandom.nextBytes(iv);

            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "BC");
            GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
            cipher.init(Cipher.ENCRYPT_MODE, masterKey, spec);

            byte[] cipherText = cipher.doFinal(plaintext.getBytes());
            return new EncryptedSecret(
                    Base64.getEncoder().encodeToString(cipherText),
                    Base64.getEncoder().encodeToString(iv)
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to encrypt secret", e);
        }
    }

    public String decrypt(String base64CipherText, String base64Iv) {
        try {
            byte[] cipherBytes = Base64.getDecoder().decode(base64CipherText);
            byte[] ivBytes = Base64.getDecoder().decode(base64Iv);

            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "BC");
            GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, ivBytes);
            cipher.init(Cipher.DECRYPT_MODE, masterKey, spec);

            byte[] plainBytes = cipher.doFinal(cipherBytes);
            return new String(plainBytes);
        } catch (Exception e) {
            throw new RuntimeException("Failed to decrypt secret", e);
        }
    }

    public record EncryptedSecret(String cipherText, String iv) {}
}

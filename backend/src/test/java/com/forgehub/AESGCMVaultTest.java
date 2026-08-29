package com.forgehub;

import com.forgehub.shared.security.AESGCMVault;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class AESGCMVaultTest {

    private final String testKeyHex = "635266556A586E3272357538782F413F4428472B4B6250645367566B5970404E";
    private final AESGCMVault vault = new AESGCMVault(testKeyHex);

    @Test
    @DisplayName("AES-256-GCM encryption and decryption roundtrip for CI secrets")
    void testEncryptDecrypt() {
        String secret = "ghp_secure_developer_collaboration_token_998877";

        AESGCMVault.EncryptedSecret enc = vault.encrypt(secret);
        assertNotNull(enc.cipherText());
        assertNotNull(enc.iv());
        assertNotEquals(secret, enc.cipherText());

        String decrypted = vault.decrypt(enc.cipherText(), enc.iv());
        assertEquals(secret, decrypted);
    }
}

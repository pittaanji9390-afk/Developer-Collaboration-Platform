from common_writer import write_file

auth_test = """package com.forgehub;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.forgehub.identity.dto.AuthDTOs.LoginRequest;
import com.forgehub.identity.dto.AuthDTOs.RegisterRequest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("dev")
public class AuthIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @DisplayName("User registration and login flow with JWT token delivery")
    void testRegisterAndLogin() throws Exception {
        String username = "dev_" + System.currentTimeMillis();
        String email = username + "@example.com";

        RegisterRequest reg = RegisterRequest.builder()
                .username(username)
                .email(email)
                .password("StrongPassword123!")
                .displayName("Developer Test")
                .build();

        mockMvc.perform(post("/api/v1/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(reg)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.accessToken").isNotEmpty())
                .andExpect(jsonPath("$.data.user.username").value(username));

        LoginRequest login = new LoginRequest(username, "StrongPassword123!");

        mockMvc.perform(post("/api/v1/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(login)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.data.accessToken").isNotEmpty())
                .andExpect(jsonPath("$.data.user.email").value(email));
    }
}
"""
write_file("backend/src/test/java/com/forgehub/AuthIntegrationTest.java", auth_test)

vault_test = """package com.forgehub;

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
"""
write_file("backend/src/test/java/com/forgehub/AESGCMVaultTest.java", vault_test)

md_test = """package com.forgehub;

import com.forgehub.shared.util.MarkdownSanitizer;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MarkdownSanitizerTest {

    private final MarkdownSanitizer sanitizer = new MarkdownSanitizer();

    @Test
    @DisplayName("Sanitize dangerous script tags and event handlers to prevent XSS")
    void testXssSanitization() {
        String malicious = "# Issue Title\\n<script>alert('XSS')</script>\\n[Click](javascript:alert(1))";
        String html = sanitizer.renderHtml(malicious);

        assertFalse(html.contains("<script>"));
        assertFalse(html.contains("javascript:"));
        assertTrue(html.contains("Issue Title"));
    }
}
"""
write_file("backend/src/test/java/com/forgehub/MarkdownSanitizerTest.java", md_test)

print("gen_phase13_tests complete.")
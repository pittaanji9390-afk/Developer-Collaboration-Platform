package com.forgehub.identity;

import com.forgehub.identity.dto.AuthDTOs.*;
import com.forgehub.shared.exception.ApiException;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.util.HexFormat;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final UserSessionRepository sessionRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenService jwtTokenService;
    private final AuthenticationManager authenticationManager;

    @Transactional
    public AuthResponse register(RegisterRequest req, HttpServletRequest request) {
        if (userRepository.existsByUsername(req.getUsername())) {
            throw ApiException.conflict("Username already taken");
        }
        if (userRepository.existsByEmail(req.getEmail())) {
            throw ApiException.conflict("Email already registered");
        }

        User user = User.builder()
                .username(req.getUsername().toLowerCase().trim())
                .email(req.getEmail().toLowerCase().trim())
                .displayName(req.getDisplayName() != null ? req.getDisplayName() : req.getUsername())
                .passwordHash(passwordEncoder.encode(req.getPassword()))
                .role(UserRole.USER)
                .status(UserStatus.ACTIVE)
                .avatarUrl("https://api.dicebear.com/7.x/identicon/svg?seed=" + req.getUsername())
                .build();

        userRepository.save(user);

        return createSessionAndResponse(user, request);
    }

    @Transactional
    public AuthResponse login(LoginRequest req, HttpServletRequest request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(req.getUsernameOrEmail(), req.getPassword())
        );

        User user = userRepository.findByUsernameOrEmail(req.getUsernameOrEmail(), req.getUsernameOrEmail())
                .orElseThrow(() -> ApiException.unauthorized("Invalid credentials"));

        user.setLastLoginAt(Instant.now());
        userRepository.save(user);

        return createSessionAndResponse(user, request);
    }

    @Transactional
    public AuthResponse refreshToken(RefreshTokenRequest req, HttpServletRequest request) {
        String hash = hashToken(req.getRefreshToken());
        UserSession session = sessionRepository.findByRefreshTokenHash(hash)
                .orElseThrow(() -> ApiException.unauthorized("Invalid refresh token"));

        if (session.isRevoked() || session.getExpiresAt().isBefore(Instant.now())) {
            throw ApiException.unauthorized("Refresh token expired or revoked");
        }

        session.setRevoked(true);
        sessionRepository.save(session);

        User user = session.getUser();
        return createSessionAndResponse(user, request);
    }

    private AuthResponse createSessionAndResponse(User user, HttpServletRequest request) {
        String accessToken = jwtTokenService.generateAccessToken(user);
        String refreshToken = jwtTokenService.generateRefreshToken(user);

        UserSession session = UserSession.builder()
                .user(user)
                .refreshTokenHash(hashToken(refreshToken))
                .userAgent(request.getHeader("User-Agent"))
                .ipAddress(request.getRemoteAddr())
                .expiresAt(jwtTokenService.extractExpiration(refreshToken).toInstant())
                .build();

        sessionRepository.save(session);

        UserSummary summary = UserSummary.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .displayName(user.getDisplayName())
                .avatarUrl(user.getAvatarUrl())
                .role(user.getRole().name())
                .build();

        return AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .tokenType("Bearer")
                .expiresIn(900)
                .user(summary)
                .build();
    }

    private String hashToken(String token) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(token.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not supported", e);
        }
    }
}

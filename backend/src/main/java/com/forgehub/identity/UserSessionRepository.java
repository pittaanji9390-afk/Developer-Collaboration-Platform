package com.forgehub.identity;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserSessionRepository extends JpaRepository<UserSession, String> {
    Optional<UserSession> findByRefreshTokenHash(String hash);
    List<UserSession> findByUserIdAndRevokedFalse(String userId);
}

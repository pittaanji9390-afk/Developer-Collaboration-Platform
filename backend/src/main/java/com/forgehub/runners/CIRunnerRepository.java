package com.forgehub.runners;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface CIRunnerRepository extends JpaRepository<CIRunner, String> {
    Optional<CIRunner> findByToken(String token);
    List<CIRunner> findByStatusAndLastPingAtAfter(CIRunner.RunnerStatus status, Instant pingThreshold);
}

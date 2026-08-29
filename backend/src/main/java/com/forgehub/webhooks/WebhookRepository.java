package com.forgehub.webhooks;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface WebhookRepository extends JpaRepository<Webhook, String> {
    List<Webhook> findByRepositoryIdAndActiveTrue(String repositoryId);
    List<Webhook> findByOrganizationIdAndActiveTrue(String organizationId);
}

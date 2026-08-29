package com.forgehub.projects;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProjectBoardRepository extends JpaRepository<ProjectBoard, String> {
    List<ProjectBoard> findByRepositoryId(String repositoryId);
    List<ProjectBoard> findByOrganizationId(String organizationId);
}

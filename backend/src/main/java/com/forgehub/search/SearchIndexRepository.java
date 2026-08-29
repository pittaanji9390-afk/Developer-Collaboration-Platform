package com.forgehub.search;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface SearchIndexRepository extends JpaRepository<SearchIndex, String> {

    @Query("SELECT s FROM SearchIndex s WHERE LOWER(s.title) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(s.content) LIKE LOWER(CONCAT('%', :query, '%'))")
    Page<SearchIndex> globalSearch(String query, Pageable pageable);

    @Query("SELECT s FROM SearchIndex s WHERE s.entityType = :type AND (LOWER(s.title) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(s.content) LIKE LOWER(CONCAT('%', :query, '%')))")
    Page<SearchIndex> searchByType(SearchIndex.SearchEntityType type, String query, Pageable pageable);
}

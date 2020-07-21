package org.trollslayer.repository;

import org.trollslayer.model.Dataset;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;


@Repository
public interface DatasetRepository extends JpaRepository<Dataset, Long> {
	
	@Query(value = "SELECT * FROM dataset WHERE user_id = ?1", nativeQuery = true)
	  List<Dataset> getDatasetsByUserId(String userId);
	
	@Query(value = "SELECT * FROM dataset WHERE file_hash = ?1", nativeQuery = true)
	  Dataset getDatasetByHash(String fileHash); 
}
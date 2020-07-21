package org.trollslayer.repository;

import org.trollslayer.model.Location;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;


@Repository
public interface LocationRepository extends JpaRepository<Location, Long> {
	
	 @Query(value = "SELECT * FROM LOCATION WHERE USER_ID = ?1", nativeQuery = true)
	  List<Location> getLocationsByUserId(String userId);
	 
	 @Query(value = "SELECT * FROM LOCATION WHERE longitude = ?1 AND latitude = ?2", nativeQuery = true)
	  List<Location> getLocationsByLongitudeLatitudeAltitude(double longitude, double latitude, double altitude);
	 
	 @Query(value = "SELECT * FROM LOCATION WHERE longitude = ?1 AND latitude = ?2", nativeQuery = true)
	  List<Location> getLocationsByLongitudeLatitude(double longitude, double latitude);
	 
	 @Query(value = "select * from location "
	 		+ "WHERE ST_Distance(geog, "
	 		+ "text_to_geom_point(:longitude, :latitude), false) "
	 		+ "<= :radius", nativeQuery = true)
	  List<Location> getLocationsByLongLatR(
			  @Param("longitude") double longitude, 
			  @Param("latitude") double latitude, 
			  @Param("radius") double radius);
}
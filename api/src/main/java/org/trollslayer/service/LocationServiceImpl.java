package org.trollslayer.service;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CompletableFuture;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import org.trollslayer.service.DatasetServiceImpl;
import org.trollslayer.model.Location;
import org.trollslayer.repository.LocationRepository;
import org.trollslayer.exception.ResourceNotFoundException;


@Service
public class LocationServiceImpl implements LocationService{
	
	@Autowired
	LocationRepository locationRepository;
	
	@Autowired
	DatasetServiceImpl datasetServiceImpl;

	@Override
	public Location saveLocation(Location location) {
		return locationRepository.save(location);
		
	}

	@Override
	public Location getLocationById(Long locationId) {
		return locationRepository.findById(locationId)
                .orElseThrow(() -> new ResourceNotFoundException("Location", "id", locationId));
	}

	@Override
	@Async
	public CompletableFuture<List<Location>> getLocations() {
		return CompletableFuture.completedFuture(locationRepository.findAll());
	}

	@Override
	public List<Location> getLocationsByUserId(String id) {
		return locationRepository.getLocationsByUserId(id);
	}
	
	@Override
	public List<Location> getLocationsByLongLatR(double longitude, double latitude, double radius) {
		return locationRepository.getLocationsByLongLatR(longitude, latitude, radius);
	}
	
	@Override
	public List<Location> getLocationsByLongitudeLatitudeAltitude(double longitude, double latitude, double altitude) {
		return locationRepository.getLocationsByLongitudeLatitudeAltitude(longitude, latitude, altitude);
	}
	
	public List<Location> generateRandomWithinCircle(double longitude, double latitude, double radius){
		double x0 = longitude;
		double y0 = latitude;
		double _radius = radius;
		
		// Convert radius from meters to degrees.
		double radiusInDegrees = _radius / 111320f;
		
		int times = 0;
		List<Location> newLocationsList = new ArrayList<Location>();
		
		// Generate 100 locations when a query for locations arrives
		while(times < 100) {
		
			Random random = new Random();
	
		    // Get a random distance and a random angle.
		    double u = random.nextDouble();
		    double v = random.nextDouble();
		    double w = radiusInDegrees * Math.sqrt(u);
		    double t = 2 * Math.PI * v;
		    // Get the x and y delta values.
		    double x = w * Math.cos(t);
		    double y = w * Math.sin(t);
	
		    // Compensate the x value.
		    double new_x = x / Math.cos(Math.toRadians(y0));
	
		    double foundLatitude;
		    double foundLongitude;
	
		    foundLatitude = y0 + y;
		    foundLongitude = x0 + new_x;
	
		    Location newLoc = new Location();
		    newLoc.setLatitude(foundLatitude);
		    newLoc.setLongitude(foundLongitude);
		    newLoc.setUserId("auto");
		    newLoc.setTimestamp(Calendar.getInstance().getTime());
		    
		    locationRepository.save(newLoc);
		    
		    times = times +1;
		    newLocationsList.add(newLoc);
		}
		return newLocationsList;
	}
	
	
	public List<Location> getLocationsByLongLatR2(double longitude, double latitude, double radius) {
		List<Location> listLoc = locationRepository.getLocationsByLongLatR(longitude, latitude, radius);
		if (listLoc.size() == 0) {
			List<Location> generatedListLoc = generateRandomWithinCircle(longitude, latitude, radius);
			return generatedListLoc;
			}
		else {return listLoc;}
	}
	
	

}

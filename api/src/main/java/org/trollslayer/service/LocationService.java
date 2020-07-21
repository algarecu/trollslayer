package org.trollslayer.service;

import java.util.List;
import java.util.concurrent.CompletableFuture;

import org.trollslayer.model.Location;

public interface LocationService {
	public abstract Location saveLocation(Location location);
	public abstract Location getLocationById(Long locationId);
	public abstract CompletableFuture<List<Location>> getLocations();
	public abstract List<Location> getLocationsByUserId(String id);
	public abstract List<Location> getLocationsByLongLatR(double longitude, double latitude, double radius);
	public abstract List<Location> getLocationsByLongitudeLatitudeAltitude(double longitude, double latitude, double altitude);
}

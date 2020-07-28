package org.trollslayer.model;

import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import javax.validation.constraints.NotBlank;
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.Id;
import javax.persistence.Temporal;
import javax.persistence.EntityListeners;
import javax.persistence.TemporalType;
import javax.persistence.GenerationType;
import javax.persistence.GeneratedValue;
import java.io.Serializable;
import java.util.Date;

@Entity
@Table(name = "location")
@EntityListeners(AuditingEntityListener.class)
//@JsonIgnoreProperties(value = {"timestamp"}, allowGetters = true)

public class Location implements Serializable {
	/**
	 * * Class for Location data model
	 */
	private static final long serialVersionUID = 1L;

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String userId;
    private double latitude;    
    private double longitude;
    private double altitude;
    
    @Temporal(TemporalType.TIMESTAMP)
    private Date timestamp;
    
	public Long getId() {
		return id;
	}


	public void setId(Long id) {
		this.id = id;
	}


	public String getUserId() {
		return userId;
	}


	public void setUserId(String userId) {
		this.userId = userId;
	}


	public double getLatitude() {
		return latitude;
	}


	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}


	public double getLongitude() {
		return longitude;
	}


	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}


	public double getAltitude() {
		return altitude;
	}


	public void setAltitude(double altitude) {
		this.altitude = altitude;
	}


	public Date getTimestamp() {
		return timestamp;
	}


	public void setTimestamp(Date timestamp) {
		this.timestamp = timestamp;
	}   
}
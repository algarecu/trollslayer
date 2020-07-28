package org.trollslayer.model;

import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import javax.persistence.*;
import javax.validation.constraints.NotBlank;

import org.apache.commons.codec.digest.DigestUtils;
import org.springframework.data.annotation.CreatedDate;
import java.io.Serializable;
import java.util.Date;

@Entity
@Table(name = "dataset")
@EntityListeners(AuditingEntityListener.class)
public class Dataset implements Serializable {
	/**
	 * * Dataset class for extracting datasets from Postgres and putting them into a {@link Channel} @TODO
	 */
	private static final long serialVersionUID = 1L;

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String userId;
    private String name;
    private double latitude;
    private double longitude;
    private double radius;
    private String filePath;
    private String fileHash;

	@Column(nullable = false, updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    @CreatedDate
    private Date timestamp;
	
	// Setters and Getters

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

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
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

	public double getRadius() {
		return radius;
	}

	public void setRadius(double radius) {
		this.radius = radius;
	}

	public String getFilePath() {
		return filePath;
	}

	public void setFilePath(String filePath) {
		this.filePath = filePath;
	}

	public Date getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(Date timestamp) {
		this.timestamp = timestamp;
	}
	public String getFileHash() {
		return fileHash;
	}

	public void setFileHash(String fileHash) {
		this.fileHash = fileHash;
	}
	
	public String generateHashFromFilePath(String filePath) {
		return DigestUtils.sha256Hex(filePath);		
	}
}
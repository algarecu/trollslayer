package org.trollslayer.model;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotBlank;

public class Tweet implements Serializable {
	/**
	 * Class for Tweet data model
	 */
	private static final long serialVersionUID = 1L;

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long tweet_id;

    @NotBlank
    private String url; // e.g., https://twitter.com/realDonaldTrump/status/1285524871666118656
    
    @Temporal(TemporalType.TIMESTAMP)
    private Date timestamp;
    
	public Long getTid() {
		return tweet_id;
	}


	public void setTid(Long tweet_id) {
		this.tweet_id = tweet_id;
	}


	public String getUserId() {
		return url;
	}


	public void setUrl(String url) {
		this.url = url;
	}

	public Date getTimestamp() {
		return timestamp;
	}


	public void setTimestamp(Date timestamp) {
		this.timestamp = timestamp;
	}   
}

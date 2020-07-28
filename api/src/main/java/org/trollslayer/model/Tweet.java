package org.trollslayer.model;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Id;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

public class Tweet implements Serializable {
	/**
	 * Class for Tweet data model
	 */
	
	public Tweet() {

    }
	
	public Tweet(long tweet_id, String user_id) {
		super();
		this.tweet_id = tweet_id;
		this.user_id = user_id;
	}
	
	public Tweet(long tweet_id) {
		this.tweet_id = tweet_id;
	}
	
	public Tweet(long tweet_id, String user_id, String url) {
		this.tweet_id = tweet_id;
		this.user_id = user_id;
		this.url = url;
	}

	private static final long serialVersionUID = 1L;

	@Id
    private Long tweet_id;
	private String user_id;
    private String url; // e.g., https://twitter.com/realDonaldTrump/status/1285524871666118656
    
    @Temporal(TemporalType.TIMESTAMP)
    private Date timestamp;
    
	public Long getTid() {
		return tweet_id;
	}
	
	public String getUid() {
		return user_id;
	}


	public void setTid(Long tweet_id) {
		this.tweet_id = tweet_id;
	}
	
	public void setUserId(String user_id) {
		this.user_id = user_id;
	}


	public String getUrl() {
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

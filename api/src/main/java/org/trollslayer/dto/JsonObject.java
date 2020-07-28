package org.trollslayer.dto;
 
// CID
// data
// channel 1: tweet_id: 1
// 			  	-> vote_id 1
// 			  	-> vote_id 2
// 			  	-> vote_id 3
//			  tweet_id: 2
// 				-> vote_id 1
// 				-> vote_id 2
// 				-> vote_id 3

public class JsonObject {
	public JsonObject(String ch_name, String tweet_id, Data data) {
		this.ch_name = ch_name;
		this.tweet_id = tweet_id;
		this.data = data;
	}

	// Setter,getters
	private Object ch_name;
	private Object tweet_id;
	private Data data;
	
	public String getTweetId() {
		return (String) tweet_id;
	}

	public void setTweetId(String tweet_id) {
		this.tweet_id = tweet_id;
	}
	
	public String getName() {
		return (String) ch_name;
	}

	public void setName(String ch_name) {
		this.ch_name = ch_name;
	}

	public Object getData() {
		return data;
	}

	public void setData(Data data) {
		this.data = data;
	}
}

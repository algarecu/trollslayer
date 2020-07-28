package org.trollslayer.model;

import java.io.Serializable;


public class Channel implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	/**
	 * Class for Channel that indexes our data model
	 * 
	 * The data structure should be like a struc in C but in Java,
	 * whereas we have multiple levels of nested structs under the Channel.
	 * 
	 * Moreless as follows, whereas data Channels can be about a specific controversial topic (e.g, guns, abortion, covid, etc).
	 * 
	 * OLD
	 * ===
	 * 
	 * index1:Channel 1 -> index1a: tweet_1 
	 * 						-> vote 1
	 * 						-> vote 2
	 * 						-> vote 3
	 * 					-> ...
	 * 					-> indexN: tweet_n
	 * 
	 * index2:Channel 2 -> index2a: tweet_2
	 * 						-> vote 1
	 * 						-> vote 2
	 * 						-> vote 3
	 * ...
	 * indexN: Channel N
	 * 
	 * 
	 * NEW
	 * ====
	 * 
	 * CID:
	 *  index1: tweet_1
	 * 				-> vote 1
	 * 				-> vote 2
	 * 				-> vote 3
	 * 
	 * IPLD for: reference list for append (ipld 'could' help for efficient updates).
	 * 
	 */
}

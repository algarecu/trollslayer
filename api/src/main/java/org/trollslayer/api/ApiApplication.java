package org.trollslayer.api;

import java.util.HashSet;
import java.util.Set;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.trollslayer.model.Tweet;

@SpringBootApplication
public class ApiApplication {

	public static void main(String[] args) {
		
		// create some predefined tweets for a mock "COVID" Topic or Channel
	    Set < Tweet > tweets_set = new HashSet < > ();
	    
	    Tweet trump = new Tweet(2L, "Corona is a fake", "");
	    Tweet hillary = new Tweet(3L, "Corona is a fact", "");
	    Tweet biden = new Tweet(4L, "Corona is a beer", "");
	    
	    tweets_set.add(trump);
	    tweets_set.add(hillary);
	    tweets_set.add(biden);
		
	    // Run the app
		SpringApplication.run(ApiApplication.class, args);
	}
}

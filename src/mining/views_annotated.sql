-- Copyright (C) 2015-2020
-- Álvaro García-Recuero, algarecu@gmail.com
--
-- This file is part of the Trollslayer framework
--
-- This program is free software: you can redistribute it and/or
-- modify it under the terms of the GNU General Public License
-- as published by the Free Software Foundation, either version 3
-- of the License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, see <http://www.gnu.org/licenses>.

-- Top-notch functions for mutual followers/followees with user MENTIONED (NOT sink_user_id). ver. 13 Jan. 2017
-- To test them:
---
--with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
--select t.tweet_id, m.mention_id, t.tweet_userid, FT_MUTUAL_FOLLOWEES_FOLLOWERS(m.mention_id, t.tweet_userid),
--FT_MUTUAL_FOLLOWERS_FOLLOWEES(m.mention_id, t.tweet_userid),
--FT_MUTUAL_FOLLOWEES(m.mention_id, t.tweet_userid), FT_MUTUAL_FOLLOWERS(m.mention_id, t.tweet_userid)
--from tmp_mentions_ids m natural join tweets t
--WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id);


-- missing annotated_all_mutual_followees_followers
create or replace view annotated_all_mutual_followees_followers as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, m.mention_id, t.tweet_userid, FT_MUTUAL_FOLLOWEES_FOLLOWERS_JACCARD(m.mention_id, t.tweet_userid) AS MUTUAL_FOLLOWEES_FOLLOWERS
from tmp_mentions_ids m natural  join tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_mutual_followees_followers;
DROP table t_annotated_abusive_mutual_followees_followers;
DROP table t_annotated_acceptable_mutual_followees_followers;
create table t_annotated_all_mutual_followees_followers as select * from annotated_all_mutual_followees_followers;
create table t_annotated_abusive_mutual_followees_followers as select * from annotated_all_mutual_followees_followers where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_mutual_followees_followers as select * from annotated_all_mutual_followees_followers where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;


-- missing annotated_all_mutual_followers_followees
create or replace view annotated_all_mutual_followers_followees as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, m.mention_id, t.tweet_userid, FT_MUTUAL_FOLLOWERS_FOLLOWEES_JACCARD(m.mention_id, t.tweet_userid) AS MUTUAL_FOLLOWERS_FOLLOWEES
from tmp_mentions_ids m natural join tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_mutual_followers_followees;
DROP table t_annotated_abusive_mutual_followers_followees;
DROP table t_annotated_acceptable_mutual_followers_followees;
create table t_annotated_all_mutual_followers_followees as select * from annotated_all_mutual_followers_followees;
create table t_annotated_abusive_mutual_followers_followees as select * from annotated_all_mutual_followers_followees where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_mutual_followers_followees as select * from annotated_all_mutual_followers_followees where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- missing annotated_all_mutual_followers
create or replace view annotated_all_mutual_followers as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_MUTUAL_FOLLOWERS_JACCARD(m.mention_id, t.tweet_userid) AS MUTUAL_FOLLOWERS
from tmp_mentions_ids m natural join tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_mutual_followers;
DROP table t_annotated_abusive_mutual_followers;
DROP table t_annotated_acceptable_mutual_followers;
create table t_annotated_all_mutual_followers as select * from annotated_all_mutual_followers;
create table t_annotated_abusive_mutual_followers as select * from annotated_all_mutual_followers where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_mutual_followers as select * from annotated_all_mutual_followers where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- annotated_all_mutual_followees
create or replace view annotated_all_mutual_followees as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, m.mention_id, t.tweet_userid, FT_MUTUAL_FOLLOWEES_JACCARD(m.mention_id, t.tweet_userid) AS MUTUAL_FOLLOWEES
from tmp_mentions_ids m natural join tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_mutual_followees;
DROP table t_annotated_abusive_mutual_followees;
DROP table t_annotated_acceptable_mutual_followees;
create table t_annotated_all_mutual_followees as select * from annotated_all_mutual_followees;
create table t_annotated_abusive_mutual_followees as select * from annotated_all_mutual_followees where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_mutual_followees as select * from annotated_all_mutual_followees where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- annotated_tweet_mentions_followees_count
create or replace view annotated_tweet_mentions_followees_count as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, u.friends_count AS followees_count
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_tweet_mentions_followees_count;
DROP table t_annotated_abuse_tweet_mentions_followees_count;
DROP table t_annotated_abuse_tweet_mentions_followees_count;
create table t_annotated_tweet_mentions_followees_count as select * from annotated_tweet_mentions_followees_count;
create table t_annotated_abuse_tweet_mentions_followees_count as select * from annotated_tweet_mentions_followees_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_abuse_tweet_mentions_followees_count as select * from annotated_tweet_mentions_followees_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- annotated_tweet_mentions_followers_count
create or replace view annotated_tweet_mentions_followers_count as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, u.followers_count AS followers_count
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_tweet_mentions_followers_count;
DROP table t_annotated_abuse_tweet_mentions_followers_count;
DROP table t_annotated_acceptable_tweet_mentions_followers_count;
create table t_annotated_tweet_mentions_followers_count as select * from annotated_tweet_mentions_followers_count;
create table t_annotated_abuse_tweet_mentions_followers_count as select * from annotated_tweet_mentions_followers_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_tweet_mentions_followers_count as select * from annotated_tweet_mentions_followers_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;
-- CF
create or replace view cf_t_annotated_tweet_mentions_followers_count as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets_cf group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, u.followers_count AS followers_count
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table cf_t_annotated_tweet_mentions_followers_count;
DROP table cf_t_annotated_abuse_tweet_mentions_followers_count;
DROP table cf_t_annotated_acceptable_tweet_mentions_followers_count;
create table cf_t_annotated_tweet_mentions_followers_count as select * from cf_t_annotated_tweet_mentions_followers_count;
create table cf_t_annotated_abuse_tweet_mentions_followers_count as select * from cf_t_annotated_tweet_mentions_followers_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table cf_t_annotated_acceptable_tweet_mentions_followers_count as select * from cf_t_annotated_tweet_mentions_followers_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;
-- TS
CREATE or REPLACE view ts_t_annotated_tweet_mentions_followers_count as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets_ts group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, u.followers_count AS followers_count
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table ts_t_annotated_tweet_mentions_followers_count;
DROP table ts_t_annotated_abuse_tweet_mentions_followers_count;
DROP table ts_t_annotated_acceptable_tweet_mentions_followers_count;
create table ts_t_annotated_tweet_mentions_followers_count as select * from ts_t_annotated_tweet_mentions_followers_count;
create table ts_t_annotated_abuse_tweet_mentions_followers_count as select * from ts_t_annotated_tweet_mentions_followers_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_ts')>1;
create table ts_t_annotated_acceptable_tweet_mentions_followers_count as select * from ts_t_annotated_tweet_mentions_followers_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_ts')<-1;

-- annotated_all_tweets_per_day
create or replace view annotated_all_tweets_per_day as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_TWEETS_PER_DAY (account_created, H_GET_POLLING_TIME(user_id), user_id) as TWEETS_PER_DAY
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_tweets_per_day;
DROP table t_annotated_abuse_tweets_per_day;
DROP table t_annotated_acceptable_tweets_per_day;
create table t_annotated_all_tweets_per_day as select * from annotated_all_tweets_per_day;
create table t_annotated_abuse_tweets_per_day as select * from annotated_all_tweets_per_day where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_tweets_per_day as select * from annotated_all_tweets_per_day where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- annotated_all_tweets_age_of_account
create or replace view annotated_all_tweets_age_of_account as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_AGE_OF_ACCOUNT (account_created, H_GET_POLLING_TIME(user_id)) as AGE_OF_ACCOUNT
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_tweets_age_of_account;
DROP table t_annotated_abusive_tweets_age_of_account;
DROP table t_annotated_acceptable_tweets_age_of_account;
create table t_annotated_all_tweets_age_of_account as select * from annotated_all_tweets_age_of_account;
create table t_annotated_abusive_tweets_age_of_account as select * from annotated_all_tweets_age_of_account where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_tweets_age_of_account as select * from annotated_all_tweets_age_of_account where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- missing annotated_all_tweet_invasive
create or replace view annotated_all_tweet_invasive as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, m.mention_id, t.tweet_userid, FT_TWEET_INVASIVE_NO_FOLLOWER_NO_FRIEND(m.mention_id, t.tweet_userid) AS TWEET_INVASIVE
from tmp_mentions_ids m natural  join tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_tweet_invasive;
DROP table t_annotated_abusive_tweet_invasive;
DROP table t_annotated_acceptable_tweet_invasive;
create table t_annotated_all_tweet_invasive as select * from annotated_all_tweet_invasive;
create table t_annotated_abusive_tweet_invasive as select * from annotated_all_tweet_invasive where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_tweet_invasive as select * from annotated_all_tweet_invasive where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Followees per day
create or replace view annotated_all_followees_sent as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, m.mention_id, t.tweet_userid,
FT_FOLLOW_R_SENT (u.account_created,H_GET_POLLING_TIME(u.user_id), u.friends_count) as RATIO_FOLLOWS_SENT
from tmp_mentions_ids m natural  join tweets t join users u on u.user_id=t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_followees_sent;
DROP table t_annotated_abusive_followees_sent;
DROP table t_annotated_acceptable_followees_sent;
create table t_annotated_all_followees_sent as select * from annotated_all_followees_sent;
create table t_annotated_abusive_followees_sent as select * from annotated_all_followees_sent where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_followees_sent as select * from annotated_all_followees_sent where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Followers per day
create or replace view annotated_all_followers_received as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, m.mention_id, t.tweet_userid,
FT_FOLLOW_R_RECEIVED (u.account_created, H_GET_POLLING_TIME(u.user_id), u.followers_count) as RATIO_FOLLOWS_RECEIVED
from tmp_mentions_ids m natural  join tweets t join users u on u.user_id=t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_followers_received;
DROP table t_annotated_abusive_followers_received;
DROP table t_annotated_acceptable_followers_received;
create table t_annotated_all_followers_received as select * from annotated_all_followers_received;
create table t_annotated_abusive_followers_received as select * from annotated_all_followers_received where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_followers_received as select * from annotated_all_followers_received where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Number of mentions
create or replace view annotated_all_number_of_mentions as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_ADDED_MENTIONS(t.tweet_text) AS MENTION_COUNT
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_number_of_mentions;
DROP table t_annotated_abusive_number_of_mentions;
DROP table t_annotated_acceptable_number_of_mentions;
create table t_annotated_all_number_of_mentions as select * from annotated_all_number_of_mentions;
create table t_annotated_abusive_number_of_mentions as select * from annotated_all_number_of_mentions where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_number_of_mentions as select * from annotated_all_number_of_mentions where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Number of hashtags
create or replace view annotated_all_number_of_hashtags as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_ADDED_HASHTAGS(t.tweet_text) AS HASHTAG_COUNT
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_number_of_hashtags;
DROP table t_annotated_abusive_number_of_hashtags;
DROP table t_annotated_acceptable_number_of_hashtags;
create table t_annotated_all_number_of_hashtags as select * from annotated_all_number_of_hashtags;
create table t_annotated_abusive_number_of_hashtags as select * from annotated_all_number_of_hashtags where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_number_of_hashtags as select * from annotated_all_number_of_hashtags where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Number of badwords
create or replace view annotated_all_number_of_badwords as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_ADDED_BADWORDS(t.tweet_text, '/Users/agarciar/Documents/github/trollrank/data/google_twunter.txt') AS BADWORDS
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_number_of_badwords;
DROP table t_annotated_abusive_number_of_badwords;
DROP table t_annotated_acceptable_number_of_badwords;
create table t_annotated_all_number_of_badwords as select * from annotated_all_number_of_badwords;
create table t_annotated_abusive_number_of_badwords as select * from annotated_all_number_of_badwords where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_number_of_badwords as select * from annotated_all_number_of_badwords where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Favourites count
create or replace view annotated_all_favourites_count as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, u.favourites_count AS FAVORITES_TWEETS
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_favourites_count;
DROP table t_annotated_abusive_favourites_count;
DROP table t_annotated_acceptable_favourites_count;
create table t_annotated_all_favourites_count as select * from annotated_all_favourites_count;
create table t_annotated_abusive_favourites_count as select * from annotated_all_favourites_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_favourites_count as select * from annotated_all_favourites_count where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Account lists
create or replace view annotated_all_account_lists as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, t.listed_count AS account_lists
FROM tweets t
-- JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP TABLE t_annotated_all_account_lists;
DROP TABLE t_annotated_abusive_account_lists;
DROP TABLE t_annotated_acceptable_account_lists;
create table t_annotated_all_account_lists as select * from annotated_all_account_lists;
create table t_annotated_abusive_account_lists as select * from annotated_all_account_lists where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_account_lists as select * from annotated_all_account_lists where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Replies over users
create or replace view annotated_all_replies_over_users as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_REPLIES_OVER_USERS (u.user_id) as REPLIES_OVER_USERS
FROM tweets t JOIN users u ON u.user_id = t.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_replies_over_users;
DROP table t_annotated_abusive_replies_over_users;
DROP table t_annotated_acceptable_replies_over_users;
create table t_annotated_all_replies_over_users as select * from annotated_all_replies_over_users;
create table t_annotated_abusive_replies_over_users as select * from annotated_all_replies_over_users where H_ABUSE_SUM(tweet_id, 'gt_tweets')>1;
create table t_annotated_acceptable_replies_over_users as select * from annotated_all_replies_over_users where H_ABUSE_SUM(tweet_id, 'gt_tweets')<-1;

-- Retweet count
create or replace view annotated_all_retweet_count as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, retweet_count AS RETWEET_COUNT
FROM tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_retweet_count;
DROP table t_annotated_abusive_retweet_count;
DROP table t_annotated_acceptable_retweet_count;
create table t_annotated_all_retweet_count as select * from annotated_all_retweet_count;
create table t_annotated_abusive_retweet_count as select * from annotated_all_retweet_count where H_ABUSE_SUM(tweet_id, 'gt_tweets')>1;
create table t_annotated_acceptable_retweet_count as select * from annotated_all_retweet_count where H_ABUSE_SUM(tweet_id, 'gt_tweets')<-1;

-- Mentions/Tweets

create or replace view annotated_all_mentions_over_tweets as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2),
 c as (select tweet_userid, count(*) as tweets_count from tweets t
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id) group by tweet_userid)
select r.tweet_id, t.tweet_userid,
(COALESCE(cast(jsonb_array_length(CAST(jsonb_extract_path_text(r.raw_tweet, 'entities', 'user_mentions')
AS JSONB)) as float), '0' )/c.tweets_count) as mentions_over_tweets
from raw_tweets r left outer join tweets t on r.tweet_id=t.tweet_id
 left outer join c on t.tweet_userid=c.tweet_userid
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_retweet_count;
DROP table t_annotated_abusive_retweet_count;
DROP table t_annotated_acceptable_retweet_count;
create table t_annotated_all_mentions_over_tweets as select * from annotated_all_mentions_over_tweets;
create table t_annotated_abusive_mentions_over_tweets as select * from t_annotated_all_mentions_over_tweets where H_ABUSE_SUM(tweet_id, 'gt_tweets')>1;
create table t_annotated_acceptable_mentions_over_tweets as select * from t_annotated_all_mentions_over_tweets where H_ABUSE_SUM(tweet_id, 'gt_tweets')<-1;

-- Annotated ratio of subscribers to subscriptions
create or replace view annotated_all_subscribers_subscriptions as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_FOLLOWERS_TO_FRIENDS (u.user_id) AS followers_to_friends
from tmp_mentions_ids m natural join tweets t JOIN users u ON t.tweet_userid=u.user_id
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_subscribers_subscriptions;
DROP table t_annotated_abusive_subscribers_subscriptions;
DROP table t_annotated_acceptable_subscribers_subscriptions;
create table t_annotated_all_subscribers_subscriptions as select * from annotated_all_subscribers_subscriptions;
create table t_annotated_abusive_subscribers_subscriptions as select * from annotated_all_subscribers_subscriptions where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_subscribers_subscriptions as select * from annotated_all_subscribers_subscriptions where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

-- Annotated ratio of subscriptions to subscribers
create or replace view annotated_all_subscriptions_subscribers as (
with annotated as (select fk_tweet_id as tweet_id from gt_tweets group by fk_tweet_id having count(*)>2)
SELECT t.tweet_id, FT_FRIENDS_TO_FOLLOWERS (u.user_id) AS friends_to_followers
from tmp_mentions_ids m natural join tweets t JOIN users u ON t.tweet_userid=u.user_id
WHERE EXISTS (select * from annotated a where t.tweet_id=a.tweet_id));

DROP table t_annotated_all_subscriptions_subscribers;
DROP table t_annotated_abusive_subscriptions__subscribers;
DROP table t_annotated_acceptable_subscriptions__subscriptions;
create table t_annotated_all_subscriptions_subscribers as select * from annotated_all_subscriptions_subscribers;
create table t_annotated_abusive_subscriptions_subscribers as select * from annotated_all_subscriptions_subscribers where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')>1;
create table t_annotated_acceptable_subscriptions_subscribers as select * from annotated_all_subscriptions_subscribers where H_ABUSE_SUM(tweet_id, 'gt_tweets_all')<-1;

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2017
# Álvaro García-Recuero, algarecu@gmail.com
#
# This file is part of the Trollslayer framework
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses>.

"""
Database layer

First creation:     April 10, 2015
Last modification:  Sunday, 6 December 2015.

__author__='algarecu'
__email__='algarecu@gmail.com'
"""

import sys
import logging
import pprint
from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, DateTime, Table, MetaData, String
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
from sqlalchemy.sql import select, and_

pp = pprint.PrettyPrinter(indent=4)
Base = declarative_base()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

#logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# CREATE SCHEMA IF NOT EXISTS `database` DEFAULT CHARACTER SET utf8mb4;
engine = create_engine("postgresql://root:@localhost/database?client_encoding=utf8")

# create scoped session
session = create_session(bind=engine, autocommit=True, autoflush=True)

# Create Meta
metadata = MetaData(engine)

# store raw tweet pointing to tweets table
raw_tweets = Table('raw_tweets', metadata,
                   Column('batch_id', INTEGER, index=True, nullable=False, autoincrement=False),
                   Column('source_user_id', BIGINT, index=True, nullable=False),
                   Column('tweet_id', BIGINT, primary_key=True, autoincrement=False, index=True, nullable=False),
                   Column('polling_time', DateTime, index=True, nullable=False),
                   Column('raw_tweet', JSONB, nullable=False),
                   Column('depth', INTEGER, index=True))

# table with followers
followers = Table('followers', metadata,
                  Column('user_id', BIGINT),
                  Column('follower_id', BIGINT),
                  PrimaryKeyConstraint('user_id', 'follower_id', name='follower_pk'))

# table with friends
friends = Table('friends', metadata,
                Column('user_id', BIGINT),
                Column('friend_id', BIGINT),
                PrimaryKeyConstraint('user_id', 'friend_id', name='friend_pk'))

# tracking last tweet_id processed for a given user_id when doing BFS traversal
cursor_tweets = Table('cursor_tweets', metadata,
                      Column('user_id', BIGINT, primary_key=True, autoincrement=False),
                      Column('next_tid', BIGINT))

# tracking last follower_id processed for a given user_id when doing BFS traversal
cursor_followers = Table('cursor_followers', metadata,
                         Column('user_id', BIGINT, primary_key=True, autoincrement=False),
                         Column('next_fid', BIGINT))

# tracking last friend_id for each given user_id when doing BFS traversal
cursor_friends = Table('cursor_friends', metadata,
                       Column('user_id', BIGINT, primary_key=True, autoincrement=False),
                       Column('next_fid', BIGINT))

# tracking the last twet annotated for each user
cursor_gt = Table('cursor_gt', metadata,
                  Column('username', String(20), ForeignKey('reviewers.reviewer_id'), index=True),
                  Column('last_tweet_id', BIGINT),
                  PrimaryKeyConstraint('username', name='cursor_gt_pk'))

# reviewers
reviewers = Table('reviewers', metadata,
                  Column('reviewer_id', String(20), primary_key=True, autoincrement=False, index=True),
                  Column('lang', String(20), nullable=True),
                  Column('geo-ip', String(20), nullable=True))

# ground-truth tweets
gt_tweets = Table('gt_tweets', metadata,
                  Column('fk_reviewer_id', String(20), ForeignKey('reviewers.reviewer_id'), index=True),
                  Column('fk_tweet_id', BIGINT, ForeignKey('raw_tweets.tweet_id'), index=True),
                  Column('abusive', String(20), default='unseen', index=True),
                  PrimaryKeyConstraint('fk_reviewer_id', 'fk_tweet_id', name='gt_tweets_pk'))

# ranks
tweet_ranks = Table('tweet_ranks', metadata,
                    Column('ranked_tweet_id', BIGINT, index=True),
                    Column('count_hashtags', INTEGER, default=0),
                    Column('count_mentions', INTEGER, default=0),
                    Column('count_replies', INTEGER, default=0),
                    Column('is_reply', BOOLEAN, default=0),
                    Column('has_reply', BOOLEAN, default=0),
                    Column('rank_tweet', DOUBLE_PRECISION, index=True, default=0.00),
                    PrimaryKeyConstraint('ranked_tweet_id', name='ranked_tweet_id'))

user_ranks = Table('user_ranks', metadata,
                   Column('ranked_user_id', BIGINT, index=True),
                   Column('avg_hashtags', NUMERIC(2, 2), default=0.00),
                   Column('avg_mentions', NUMERIC(2, 2), default=0.00),
                   Column('h_avg_p', NUMERIC(2, 2), default=0.00),  # avg hashtag proximity
                   Column('m_avg_p', NUMERIC(2, 2), default=0.00),  # avg mention proximity
                   Column('rank_user', DOUBLE_PRECISION, index=True, default=0.00),
                   PrimaryKeyConstraint('ranked_user_id', name='ranked_user_id'))

# %%%%%%%%%%%%%%%%%%%%% Tables to create match from jsonb %%%%%%%%%%%%%%%%%%%%% #

# Table with users
users = Table('users', metadata,
              Column('user_id', BIGINT, primary_key=True, autoincrement=False, index=True, nullable=False),
              Column('name', String(40)),
              Column('screen_name', String(40), default=True),
              Column('followers_count', BIGINT, default=False),
              Column('friends_count', BIGINT, default=False),
              Column('favourites_count', BIGINT, default=False),
              Column('tweet_count', INTEGER, default=False),
              Column('user_lang', String(5), default=False),
              Column('polling_time', DateTime, default=False, index=True),
              Column('account_created', DateTime, default=False),
              Column('account_status', BOOLEAN, default=True),
              Column('account_verified', BOOLEAN, default=False),
              Column('depth', INTEGER)
              )

seeds = Table('seeds', metadata,
              Column('user_id', BIGINT, primary_key=True, autoincrement=False, index=True, nullable=False),
              Column('name', String(40)),
              Column('screen_name', String(40), default=True),
              Column('followers_count', BIGINT, default=False),
              Column('friends_count', BIGINT, default=False),
              Column('favourites_count', BIGINT, default=False),
              Column('tweet_count', INTEGER, default=False),
              Column('user_lang', String(5), default=False),
              Column('polling_time', DateTime, default=False, index=True),
              Column('account_created', DateTime, default=False),
              Column('account_status', BOOLEAN, default=True),
              Column('account_verified', BOOLEAN, default=False),
              Column('depth', INTEGER)
              )

skipped = Table('skipped', metadata,
                Column('user_id', BIGINT, primary_key=True, autoincrement=False, index=True, nullable=False),
                Column('reason', String(40), index=True))

# Table with tweets to annotate
annotated_tweets = Table('annotated_tweets', metadata,
                         Column('tweet_id', BIGINT, primary_key=True, autoincrement=False, index=True, nullable=False),
                         Column('tweet_text', String(150), unique=False, default=True),
                         Column('tweet_creation', DateTime, nullable=False),
                         Column('tweet_userid', BIGINT, index=True),
                         Column('in_reply_to_tweet_id', BIGINT, index=True, nullable=False),
                         Column('retweet_count', INTEGER, default=0),
                         Column('retweet', BOOLEAN, default=False),
                         Column('possibly_sensitive', BOOLEAN, default=False),
                         Column('listed_count', INTEGER, default=0),
                         Column('mentions', JSONB),
                         Column('hashtags', JSONB),
                         Column('depth', INTEGER),
                         Column('msg_type', CHAR),
                         Column('polling_time', DateTime, default=False))

# Table with tweets
tweets = Table('tweets', metadata,
               Column('tweet_id', BIGINT, primary_key=True, autoincrement=False, nullable=False),
               Column('tweet_text', String(150), unique=False, default=True),
               Column('tweet_creation', DateTime, nullable=False),
               Column('tweet_userid', BIGINT, ForeignKey('users.user_id'), index=True),
               Column('in_reply_to_tweet_id', BIGINT, index=True, nullable=True),
               Column('retweet_count', INTEGER, default=0),
               Column('retweet', BOOLEAN, default=False),
               Column('tweet_lang', VARCHAR, default=False),
               Column('possibly_sensitive', BOOLEAN, default=False),
               Column('listed_count', INTEGER, default=0),
               Column('mentions', JSONB),
               Column('hashtags', JSONB),
               Column('depth', INTEGER, index=True),
               Column('msg_type', CHAR, index=True),
               Column('polling_time', DateTime, default=False, index=True))

# We need this line or tables are not created with right metadata
metadata.create_all()

class DBRawTweets(object):
    def __init__(self, batch_id, source_user_id, tweet_id, polling_time, raw_tweet, depth):
        """
        Table to store raw tweets
        :return:
        """
        self.batch_id = batch_id
        self.source_user_id = source_user_id
        self.tweet_id = tweet_id
        self.polling_time = polling_time
        self.raw_tweet = raw_tweet
        self.depth = depth


class DBUser(object):
    def __init__(self, user_id, name, screen_name, followers_count, friends_count, favourites_count, tweet_count,
                 user_lang, polling_time, account_created, account_active, verified, depth):
        """
        @param user_id:
        @param name:
        @param screen_name:
        @param followers_count:
        @param friends_count:
        @param tweet_count:
        @param user_lang:
        @param polling_time:
        @param account_created:
        @param account_active:
        @param verified:
        @param depth:
        """
        self.user_id = user_id
        self.name = name
        self.screen_name = screen_name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.favourites_count = favourites_count
        self.tweet_count = tweet_count
        self.user_lang = user_lang
        self.polling_time = polling_time
        self.account_created = account_created
        self.account_active = account_active
        self.verified = verified
        self.depth = depth

    def getUserId(self):
        """
        Getter id
        @return: the user
        """
        return self.user_id

    def getUserName(self):
        """
        Getter name
        @return:
        """
        return self.name

    def getScreenName(self):
        """
        Getter for screen_name
        @return:
        """
        return self.screen_name

    def getFollowersCount(self):
        """
        Getter for followers_count
        @return:
        """
        return self.followers_count

    def getFriensCount(self):
        """
        Getter for friends_count
        @return:
        """
        return self.friends_count

    def getTweetsCount(self):
        return self.tweet_count

    def getLanguage(self):
        return self.user_lang

    def getAccountData(self):
        return self.account_created

    def getAccountStatus(self):
        """
        Getter for account_status
        @return: BOOLEAN
        """
        return self.account_active

    def getVerified(self):
        """
        Getter for verified
        @return: BOOLEAN
        """
        return self.verified

class DBSeeds(DBUser):
    def __init__(self, uid, name, s_name, followers, friends, favorites, tweets, user_lang, poll, created_at, active,
                 verified, depth):
        super(DBSeeds, self).__init__(uid, name, s_name, followers, friends, favorites, tweets, user_lang, poll,
                                      created_at, active, verified, depth)

    def getUserId(self):
        """
        Getter id
        @return: the user
        """
        return self.user_id

    def getUserName(self):
        """
        Getter name
        @return:
        """
        return self.name

    def getScreenName(self):
        """
        Getter for screen_name
        @return:
        """
        return self.screen_name

    def getFollowersCount(self):
        """
        Getter for followers_count
        @return:
        """
        return self.followers_count

    def getFriensCount(self):
        """
        Getter for friends_count
        @return:
        """
        return self.friends_count

    def getTweetsCount(self):
        return self.tweet_count

    def getLanguage(self):
        return self.user_lang

    def getAccountData(self):
        return self.account_created

    def getAccountStatus(self):
        """
        Getter for account_status
        @return: BOOLEAN
        """
        return self.account_active

    def getVerified(self):
        """
        Getter for verified
        @return: BOOLEAN
        """
        return self.verified

    def getUserId(self):
        """
        Getter id
        @return: the user
        """
        return self.user_id

    def getUserName(self):
        """
        Getter name
        @return:
        """
        return self.name

    def getScreenName(self):
        """
        Getter for screen_name
        @return:
        """
        return self.screen_name

    def getFollowersCount(self):
        """
        Getter for followers_count
        @return:
        """
        return self.followers_count

    def getFriensCount(self):
        """
        Getter for friends_count
        @return:
        """
        return self.friends_count

    def getTweetsCount(self):
        return self.tweet_count

    def getLanguage(self):
        return self.lang_iso

    def getAccountData(self):
        return self.account_created

    def getAccountStatus(self):
        """
        Getter for account_status
        @return: BOOLEAN
        """
        return self.account_active

    def getVerified(self):
        """
        Getter for verified
        @return: BOOLEAN
        """
        return self.verified


class DBNextFollower(object):
    def __init__(self, user_id, next_fid):
        self.user_id = user_id
        self.next_fid = next_fid

    def getUserId(self):
        return self.user_id

    def getNextFollowerId(self):
        return self.next_fid


class DBNextFriend(object):
    def __init__(self, user_id, next_fid):
        self.user_id = user_id
        self.next_fid = next_fid

    def getUserId(self):
        return self.user_id

    def getNextFriendId(self):
        return self.next_fid


class DBTweet(object):
    """
    Saving tweets object mapper

    @:param tweet_id: identifier of tweet
    @:param tweet_text: text of tweet
    @:param tweet_creation: date of publication of tweet
    @:param tweet_userid: id of tweet author
    @:param in_reply_to_tweet_id: identifier of tweet replied
    @:param retweet_count: number of retweets
    @:param retweet: check if it is a retweet
    @:param possibly_sensitive: check if a URL contained in the tweet has media identified as sensitive content
    @:param listed_count: number of lists the author of the tweet is subscribed to
    @:param mentions: array of mentions
    @:param hashtags: array of hashtags
    @:param depth: level at which the tweet was found, from [0 to 3]
    @:param msg_type: m (mention), r (reply), n (none)
    @param polling_time: when was the tweet pulled from the API
    """

    def __init__(self, tweet_id, tweet_text, tweet_creation, tweet_userid, in_reply_to_tweet_id, retweet_count, retweet,
                 tweet_lang, possibly_sensitive, listed_count, mentions, hashtags, depth, msg_type, polling_time):
        self.tweet_id = tweet_id
        self.tweet_text = tweet_text
        self.tweet_creation = tweet_creation
        self.tweet_userid = tweet_userid
        self.in_reply_to_tweet_id = in_reply_to_tweet_id
        self.retweet_count = retweet_count
        self.retweet = retweet
        self.tweet_lang = tweet_lang
        self.possibly_sensitive = possibly_sensitive
        self.listed_count = listed_count
        self.mentions = mentions
        self.hashtags = hashtags
        self.depth = depth
        self.msg_type = msg_type
        self.polling_time = polling_time

    def getTweetId(self):
        return self.tweet_id

    def getTweetText(self):
        return self.tweet_text

    def getCreatedAt(self):
        return self.tweet_creation

    def getTweetUser(self):
        return self.tweet_userid

    def getReplyToId(self):
        return self.in_reply_to_tweet_id

    def getDepth(self):
        return self.depth


class DBNextTweet(object):
    def __init__(self, user_id, next_tid):
        self.user_id = user_id
        self.next_tid = next_tid

    def getUserId(self):
        return self.user_id

    def getNextTweetId(self):
        return self.next_tid

class DBFollowers(object):
    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id


class DBFriends(object):
    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id


class DBGTtweets(object):
    def __init__(self, fk_reviewer_id, fk_tweet_id, tweet_creation, abusive):
        self.fk_reviewer_id = fk_reviewer_id
        self.fk_tweet_id = fk_tweet_id
        self.tweet_creation = tweet_creation
        self.abusive = abusive


class DBReviewers(object):
    def __init__(self, reviewer_id, age, geo):
        self.reviewer_id = reviewer_id
        self.age = age
        self.geo = geo


class DBTweetRanks(object):
    def __init__(self, ranked_tweet_id, count_hashtags, count_mentions, count_replies, is_reply, has_reply, rank_tweet):
        self.ranked_tweet_id = ranked_tweet_id
        self.count_hashtags = count_hashtags
        self.count_mentions = count_mentions
        self.count_replies = count_replies
        self.is_reply = is_reply
        self.has_repy = has_reply
        self.rank_tweet = rank_tweet


class DBUserRanks(object):
    def __init__(self, ranked_user_id, avg_hashtags, avg_mentions, h_avg_p, m_avg_p, rank_user):
        self.ranked_user_id = ranked_user_id
        self.avg_hashtags = avg_hashtags
        self.avg_mentions = avg_mentions
        self.h_avg_p = h_avg_p
        self.m_avg_p = m_avg_p
        self.rank_user = rank_user


class DBSuspended(object):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class DBSkipped(object):
    def __init__(self, user_id, reason):
        self.user_id = user_id
        self.reason = reason


class DBGtcursor(object):
    def __init__(self, username, last_tweet_id):
        self.username = username
        self.last_tweet_id = last_tweet_id

    def getUsername(self):
        return self.username

    def getLastTweetId(self):
        return self.last_tweet_id


mapper(DBRawTweets, raw_tweets)
mapper(DBFollowers, followers)
mapper(DBFriends, friends)
mapper(DBNextTweet, cursor_tweets)
mapper(DBNextFollower, cursor_followers)
mapper(DBNextFriend, cursor_friends)
mapper(DBReviewers, reviewers)
mapper(DBGTtweets, gt_tweets)
mapper(DBTweetRanks, tweet_ranks)
mapper(DBUserRanks, user_ranks)
mapper(DBUser, users)
mapper(DBSeeds, seeds)
mapper(DBTweet, tweets)
mapper(DBSkipped, skipped)
mapper(DBGtcursor, cursor_gt)


class Database():
    """
    Database class and methods it contains
    """

    def saveRawTweet(self, batch_id, source_user_id, tweet_id, polling_time, raw_tweet, depth):
        """
        Saves raw tweet in database

        :param: batch_id, source_user_id, tweet_id, polling_time, raw_tweet in json
        :return:
        """
        id = self.findRawTweetById(tweet_id)
        if id:
            print >> sys.stdout, 'Tweet %d already exists...', id
        else:
            raw_tweet_to_insert = DBRawTweets(batch_id, source_user_id, tweet_id, polling_time, raw_tweet, depth)
            session.add(raw_tweet_to_insert)
            session.flush()

    def findAllUsersMaxFollowers(self, maximum_followers=1000):
        """
        Find all users under maxFollowers threshold that have same number or higher followers than friends
        """
        return session.query(DBUser).filter(DBUser.followers_count >= DBUser.friends_count).filter(
            DBUser.followers_count <= maximum_followers).all()

    def saveUser(self, uid, name, s_name, followers, friends, favorites, tweets, user_lang, poll, created_at, active,
                 verified, depth):
        """
        Saves a User in the databases
        :param uid:
        :param name:
        :param s_name:
        :param followers:
        :param friends:
        :param favorites:
        :param tweets:
        :param user_lang: language of the user profile
        :param poll:
        :param created_at:
        :param active:
        :param verified:
        :param depth:
        :return:
        """
        user = self.findUserById(uid)
        if user:
            logger.info('User %d already exists... update it' % uid)
            self.updateUser(uid, name, s_name, followers, friends, favorites, tweets, user_lang, created_at, active,
                            verified, depth)

        else:
            user = DBUser(uid, name, s_name, followers, friends, favorites, tweets, user_lang, poll, created_at, active,
                          verified, depth)
            session.add(user)
            session.flush()

    def saveSeed(self, uid, name, s_name, followers, friends, favorites, tweets, user_lang, poll, created_at, active,
                 verified, depth):
        '''

        :param uid:
        :param name:
        :param s_name:
        :param followers:
        :param friends:
        :param favorites:
        :param tweets:
        :param user_lang:
        :param poll:
        :param created_at:
        :param active:
        :param verified:
        :param depth:
        :return:
        '''

        user = DBSeeds(uid, name, s_name, followers, friends, favorites, tweets, user_lang, poll, created_at, active,
                      verified, depth)
        session.add(user)
        session.flush()

    def saveUserSkipped(self, uid, reason):
        """
        Function to see how often a user's timeline or account is not scanned, due to protected timeline (401),
        suspended account (403), deleted account (404) or skipped account (maxfollowers).

        :param uid:
        :param reason: protected, suspended, deleted or maxfollowers
        """

        user = self.findUserById(uid)
        if user:
            print >> sys.stdout, 'User details of %d already exists in users table, saving...', user

        user = DBSkipped(uid, reason)
        session.add(user)
        session.flush()

    def saveSuspendedUser(self, name):
        """
        Saves users suspended in mentions
        @param name: screen_name of user suspended
        @return:
        """
        suspended = DBSuspended(name)
        session.add(suspended)
        session.flush()

    def updateUser(self, uid, name, s_name, followers, friends, favorites, tweets, user_lang, created_at, active,
                   verified, depth):
        """
        Update user in users table
        :param uid:
        :param name:
        :param s_name:
        :param followers:
        :param friends:
        :param favorites:
        :param tweets:
        :param user_lang:
        :param poll: polling_time field in users
        :param created_at:
        :param active:
        :param verified:
        :param depth:
        :return:
        """
        print >> sys.stdout, 'Updating user with uid [%s]' % uid
        session.query(DBUser).filter(DBUser.user_id == uid).update({'name': name,
                                                                    'screen_name': s_name,
                                                                    'followers_count': followers,
                                                                    'friends_count': friends,
                                                                    'favourites_count': favorites,
                                                                    'tweet_count': tweets,
                                                                    'user_lang': user_lang,
                                                                    'account_created': created_at,
                                                                    'account_status': active,
                                                                    'account_verified': verified,
                                                                    'depth': depth})

    def updateUserFavorites(self, uid, favorites):
        """
        Update favorites_count User in the database
        """
        print >> sys.stderr, 'Updating user %i with %s favorites' % (uid, favorites)
        session.query(DBUser).filter(DBUser.user_id == uid).update({'favourites_count': favorites})

    def updateUserDepth(self, uid, depth):
        """
        Update depth of User in database
        """
        print >> sys.stdout, 'Updating user %i with %s depth' % (uid, depth)
        session.query(DBUser).filter(DBUser.user_id == uid).update({'depth': depth})

    def saveTweet(self, tid, text, creation, referred_uid, in_reply_to_tweet_id, retweet_count, retweet, tweet_lang,
                  possibly_sensitive, listed_count, mentions, hashtags, depth, msg_type, polling_time):
        """
        Saves a Tweet in the database
        """
        tweet = self.findTweetById(tid)
        if not tweet:
            tweet = DBTweet(tid, text, creation, referred_uid, in_reply_to_tweet_id, retweet_count, retweet, tweet_lang,
                            possibly_sensitive, listed_count, mentions, hashtags, depth, msg_type, polling_time)
            session.add(tweet)
            session.flush()

    def saveNextTweet(self, uid, next_tid):
        """
        Save cursor in cursor_tweets for next tweet of user
        @param user_id: current user
        @param next_tid: next tweet_id
        """
        next_tid_user = session.query(DBNextTweet).filter_by(user_id=uid).first()
        if next_tid_user is None:
            tweet = DBNextTweet(uid, next_tid)
            session.add(tweet)
            session.flush()
        else:
            # logger.warn("Need to update cursor_tweet: row exists but empty")
            self.updateNextTWeet(uid, next_tid)
        session.flush()

    def updateNextTWeet(self, uid, next_tid):
        """
        Update the cursor in cursor_tweets
        @param uid: current user_id
        @param next_tid: next tweet_id cursor value
        """
        next_tid_user = session.query(DBNextTweet).filter_by(user_id=uid).first()

        if next_tid_user is None:
            tweet = DBNextTweet(uid, next_tid)
            session.add(tweet)
        else:
            session.query(DBNextTweet).filter(DBNextTweet.user_id == uid).update({'next_tid': next_tid})
        session.flush()

    def saveNextFollower(self, user_id, next_fid):
        """
        Save cursor in cursor_followers
        @param user_id: current user_id
        @param next_fid: next follower_id cursor value
        """
        follower = DBNextFollower(user_id, next_fid)
        session.add(follower)
        session.flush()

    def getNextFollower(self, user_id):
        """
        Get cursor in cursor_followers
        :param user_id:
        :param next_fid:
        :return: True (not 0) or False (0)
        """
        q = session.query(DBNextFollower.next_fid).filter(DBNextFollower.user_id == user_id)
        if q != 0:
            return True
        else:
            return False

    def getNextFollowee(self, user_id):
        """
        Get cursor in cursor_followers
        :param user_id:
        :param next_fid:
        :return: True (not 0) or False (0)
        """
        q = session.query(DBNextFriend.next_fid).filter(DBNextFriend.user_id == user_id)
        if q != 0:
            return True
        else:
            return False

    def updateNextFollower(self, user_id, next_fid):
        """
        Update the cursor in cursor_followers
        @param user_id: current user_id
        @param next_fid: next follower_id cursor value
        """
        session.query(DBNextFollower).filter(DBNextFollower.user_id == user_id).update({'next_fid': next_fid})
        session.flush()

    def saveNextFriend(self, user_id, next_fid):
        """
        Save cursor to next friend for a given user
        @param user_id: current user_id
        @param next_fid: next follower_id cursor value
        """
        friend = DBNextFriend(user_id, next_fid)
        session.add(friend)

    def updateNextFriend(self, user_id, next_fid):
        """
        Update the cursor in cursor_followers
        @param user_id: current user_id
        @param next_fid: next follower_id cursor value
        """
        session.query(DBNextFriend).filter(DBNextFriend.user_id == user_id).update({'next_fid': next_fid})
        session.flush()

    def findUserById(self, user_id):
        """
        Find user by user_id in the users table
        @param id: searched user_id
        """
        q = session.query(DBUser).filter(DBUser.user_id == user_id)
        if session.query(func.count(q) == 1):
            searched_user_id = session.query(DBUser).get(user_id)
            return searched_user_id
        else:
            return False

    def findUserByIdProtected(self, user_id):
        """
        Find user by user_id in the users table
        @param id: searched user_id
        """
        q = session.query(DBSkipped).filter(DBSkipped.user_id == user_id)
        if session.query(func.count(q) == 1):
            searched_user_id = session.query(DBSkipped).get(user_id)
            return searched_user_id
        else:
            return False

    def findReviewerById(self, reviewer_id):
        """
        Find reviewer by id in the reviewers table
        """
        q = session.query(DBReviewers).filter(DBReviewers.reviewer_id == id)
        if session.query(func.count(q) == 1):
            reviewer_id = session.query(DBReviewers).get(reviewer_id)
            return reviewer_id
        else:
            return False

    def createUserId(self, id):
        """
        Create reply_to id
        """
        q = session.query(DBUser).filter(DBUser.user_id == id)
        if session.query(func.count(q) == 0):
            session.query(DBUser).update()

    def findUserByName(self, screen_name):
        """
        Find user by id in the database
        """
        q = session.query(DBUser).filter(DBUser.screen_name == screen_name)
        if session.query(func.count(q) == 1):
            username = session.query(DBUser).get(screen_name)
            return username
        else:
            return False

    def findTweetById(self, tid):
        """
        Find tweet by id in the database
        """
        t = session.query(DBTweet).filter(DBTweet.tweet_id == tid)
        if session.query(func.count(t) == 1):
            tweetid = session.query(DBTweet).get(tid)
            return tweetid
        else:
            return False

    def findTweetById(self, tid):
        """
        Find tweet by id in the database
        """
        t = session.query(DBTweet).filter(DBTweet.tweet_id == tid)
        if session.query(func.count(t) == 1):
            tweetid = session.query(DBTweet).get(tid)
            return tweetid
        else:
            return False

    def findRawTweetById(self, tid):
        """
        Find raw tweet by id in the database
        """
        t = session.query(DBRawTweets).filter(DBRawTweets.tweet_id == tid)
        if session.query(func.count(t) == 1):
            tweetid = session.query(DBRawTweets).get(tid)
            return tweetid
        else:
            return False

    def findLowestTweetByUserId(self, uid):
        """
        Find the lowest tweet_id tracked in db from a given user
        """
        t = session.query(DBTweet).filter(DBTweet.tweet_userid == uid)

        if session.query(func.count(t) > 1):
            print("1 Tweet or more")
            query = session.query(func.max(DBTweet.tweet_id).label("max_tweet_id"))
            min = query.one()

        elif session.query(func.count(t) == 1):
            print("1 Tweet only")
            query = session.query(DBTweet).filter(DBTweet.tweet_userid == uid)
            min = query.one()
        else:
            print("No tweet for user in db")
            min = None
        return min

    def findNextTweetByUid(self, uid):
        """
        Find next_tweet cursor by uid in database
        """
        for tweet, in session.query(DBNextTweet.next_tid).filter(DBNextTweet.user_id == uid):
            return tweet

    def findNextFollowerByUid(self, uid):
        """
        Find next follower cursor by uid in table cursor_followers
        """

        for follower, in session.query(DBNextFollower.next_fid).filter(DBNextFollower.user_id == uid):
            return follower

    def findNextFriendByUid(self, uid):
        """
        Find next friend cursor by uid in table cursor_friends
        """
        for friend, in session.query(DBNextFriend.next_fid).filter(DBNextFriend.user_id == uid):
            return friend

    def checkUserExists(self, id):
        """
        Check if user exist before adding to db
        """
        userid = self.findUserById(id)
        if userid:
            return True
        else:
            return False

    def checkReviewerId(self, id):
        """
        Function to check if a reviewer id entered exists
        """
        reviewer_id = self.findReviewerById(id)
        if reviewer_id:
            return reviewer_id
        else:
            return False

    def updateDb(self, id, table_name):
        """
        Update existing user record in db
        """
        if table_name == 'users':
            u = session.query(DBUser).get(id)
            if session.query(func.count(u) == 1):
                # session.query(DBUser).filter(DBUser.user_id==id)
                return True
            else:
                return False

        elif table_name == 'tweets':
            t = session.query(DBTweet).get(id)
            if session.query(func.count(t) == 1):
                return True
            else:
                return False

    def checkUserInFollowers(self, uid, fid):
        """
        See if a given user id exist in followers
        :rtype: bool
        """
        key_user = False

        for u, in session.query(DBFollowers.user_id).filter(and_(DBFollowers.user_id == uid, DBFollowers.follower_id == fid)):
            key_user = True

        if key_user:
            logger.info("Follower tuple exist")
            return True
        else:
            return False

    def checkUserInFollowees(self, uid, fid):
        """
        See if a given user id exist in followees
        :rtype: bool
        """
        key_user = False

        for u, in session.query(DBFriends.user_id).filter(and_(DBFriends.user_id == uid, DBFriends.friend_id == fid)):
            key_user = True

        if key_user:
            logger.info("Friend tuple exist")
            return True
        else:
            return False

    def saveFollowersList(self, parent={}):
        """
        Function to save followers
        """
        for k, v in parent.iteritems():
            if self.checkUserInFollowers(k, v):
                return
            else:
                follower = DBFollowers(v, k)
                session.add(follower)
                session.flush()

    def saveFollower(self, parent, user):
        """
        Function to save a follower
        :param parent:
        :param user:
        """
        if self.checkUserInFollowers(parent, user):
            logger.info('Follower already in database')
        else:
            follower = DBFollowers(parent, user)
            session.add(follower)
            session.flush()

    def saveFriend(self, parent, user):
        """
        Function to save 1 friend
        :param parent:
        :param user:
        """
        if self.checkUserInFollowees(parent, user):
            logger.info('Followee already in database')
        else:
            friend = DBFriends(parent, user)
            session.add(friend)
            session.flush()

    def saveFriends(self, parent):
        """
        Function to save friends
        """
        for k, v in parent.iteritems():
            friend = DBFriends(v, k)
            session.add(friend)
            session.flush()

    def getTweetIdsGt(self):
        ids = session.query(DBGTtweets.fk_tweet_id).all()
        return ids

    def getBatchId(self):
        """
        Function to get latest id from batch id's in database
        :return: batch_id, int
        """
        query = session.query(func.max(DBRawTweets.batch_id).label("max_batch_id"))
        res = query.one()
        max_id = res.max_batch_id

        if max_id is None:
            return 1
        else:
            return max_id + 1

    def flush(self):
        """
        saves everything from the current session
        """
        session.commit()

    def close(self):
        """
        close the session properly
        """
        session.close()
database = Database()

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
Ground-truth reader

Created on '26/05/15'
__author__='algarecu'
__email__='algarecu@gmail.com'
"""

import getch
import textwrap
import os
import sys
import argparse
import traceback
import src.utils.colors_function as colors
import src.mining.database as db
from sqlalchemy import func, Table
from sqlalchemy.sql import select, and_, desc
from src.mining.crawler_twitter import CrawlerTwitter
from src.mining.database import engine, gt_tweets, reviewers, tweet_ranks, cursor_gt, database
from src.mining.database import tweets, replies
from colorama import init

init( strip=not sys.stdout.isatty( ) )  # strip colors if stdout is redirected
from termcolor import cprint, colored
from pyfiglet import figlet_format
from src.utils.get_api_keys import get_api_keys as gk

text_guidelines = 'To mark a tweet as abuse, we ask you to read the JTRIG techniques for online HUMINT Operations.\n'

header = "\n#### JTRIG 4 D's: Deny, Disrupt, Degrade or Deceive: \n\n"
bullets = "- Deny: encouraging self-harm to others users, promoting violence (direct or indirect), terrorism or \n" \
          "similar activities.\n\n" + \
          "- Disrupt: distracting provocations, denial-of-service, flooding with messages, promote abuse.\n\n" + \
          "- Degrade: disclosing personal and private data of others without their approval as to harm their public \n" \
          "image/reputation.\n\n" + \
          "- Deceive: supplanting a known user identity (impersonation) for influencing other users behavior and \n" \
          "activities, including assuming false identities (but not pseudonyms).\n\n"

example_tweet = "\nTweet:"
example_abuse = "\tI retract my awful statement of #XXXX people with batman/anime/Sin City avatars deserve death.\n" \
                "\tI really meant ”frozen in time forever”. \n\n"
login = "Please enter your id below, choose something unique and that you can remember (annotations are grouped by id):"
login_warning = "If you have already annotated data, please reuse your unique identifier to continue annotations"
login_exit = "To exit: Ctrl + C"

tweet = colored(example_tweet, 'magenta')
abuse = colored(example_abuse, 'magenta')
warning = colored(login_warning, 'red', attrs=['blink'])

def cls_next_tweet():
    """
    Function to reprint the header of the tool
    @return:
    """
    os.system(['clear', 'cls'][os.name == 'nt'])
    cprint(header, "red")
    cprint(bullets)

def cls():
    """
    Function to reprint the header of the tool
    @return:
    """
    os.system(['clear', 'cls'][os.name == 'nt'])
    # cprint(header, "red")
    # cprint(bullets)

def print_banner():
    """
    Print TrollSlayer header
    :return:
    """
    cls()
    cprint(figlet_format('TrollSlayer', font='basic', width='90'), 'grey', attrs=['bold', 'concealed'], end='\n')
    # cprint(figlet_format('Welcome, happy troll hunting', font='thin'), 'grey', attrs=['bold'])
    cprint(text_guidelines)
    cprint(header, "red")
    cprint(bullets)
    cprint('Abusive tweet matching Deny', 'red', attrs=['underline'])
    cprint(tweet + abuse)
    cprint(login)
    cprint(warning)
    cprint(login_exit)

def anonimize_users(data):
    """
    Function to remove user ids from tweets we annotate
    @param data: tweet text
    @return: curated text
    """
    words = data.split( )
    for k, v in enumerate( words ):
        if '@' in v:
            words[k] = '@user'

    data_curated = ' '.join(str(elem) for elem in words)
    return data_curated


def print_replies(data, author, crawler):
    """
    Function to get replies to the current tweet being annotated
    @return:
    """
    if data > 0:
        for row in data:
            tweet_id = unicode(row['tweet_id']).encode('utf-8')
            id_reply = unicode(row['in_reply_to_tweet_id']).encode('utf-8')
            user_id_reply = unicode(row['tweet_userid'])
            text_reply = unicode(row['tweet_text']).encode('utf-8')
            text_reply = anonimize_users(text_reply)
            reply_date = row['tweet_creation']

            if reply_date is None:
                full_tweet = crawler.show_status( id=tweet_id )
                crawler.handle_rate_limit('statuses', 'statuses/show/:id' )

                reply_date = crawler.convert_to_datetime(full_tweet['created_at'])
                db.database.updateReplyDate(reply_date, tweet_id)

            if id != id_reply:
                if author == user_id_reply:
                    print >> sys.stdout, '{.FGMAGENTA}'.format(colors.bcolors) + str(reply_date) \
                                         + " ----> self-reply: " + '{.ENDC}'.format( colors.bcolors), text_reply
                else:
                    print >> sys.stdout, '{.FGMAGENTA}'.format(colors.bcolors) + str(reply_date) \
                                         + " ----> reply: " + '{.ENDC}'.format(colors.bcolors), text_reply


def print_in_reply_to(data, crawler):
    """
    Function to get source tweet if current tweet is a in-reply-to.
    @return:
    """

    if data:
        # id of the in_reply_to
        id_tweet = unicode( data['tweet_id'] ).encode( 'utf-8' )
        id_tweet_date = data['tweet_creation']

        if id_tweet_date is None:
            full_in_reply = crawler.show_status( id=id_tweet )
            id_tweet_date = crawler.convert_to_datetime( full_in_reply['created_at'] )

        l1_reply = unicode( data['tweet_text'] ).encode('utf-8')
        l1_reply = anonimize_users(l1_reply)

        print >> sys.stdout, '{.FGMAGENTA}'.format( colors.bcolors ) + str(id_tweet_date) \
                             + " ----> in_reply_to:" + '{.ENDC}'.format(colors.bcolors), l1_reply


def print_bordered_text(text, tweet_date):
    """
    Function to print tweet with border
    :param date: the tweet date
    :param text: the tweet text
    :return:
    """
    maxlen = max(len(s) for s in text)
    colwidth = maxlen + 2

    print '+' + '-' * colwidth + '+'
    for s in my_text_frame:
        print '{.FGMAGENTA}'.format(colors.bcolors) + str(tweet_date) + " :\t" + \
              '%-*.*s' % (maxlen, maxlen, s) + '{.ENDC}'.format(colors.bcolors)
    print '+' + '-' * colwidth + '+'


def my_text_frame(string_lst, tweet_date, width=160):

    g_line = "+{0}+".format("-"*(width-2))

    print g_line
    print '{.FGMAGENTA}'.format(colors.bcolors) + str(tweet_date) + " :\t" + ' %-*.*s ' % (width, width, string_lst) + '{.ENDC}'.format(colors.bcolors)
    print g_line

def get_context(tweet, conn, tweet_type, crawler, *args):
    """
    Function to display context of user tweet
    @param: tweet_id, user_id
    @return:
    """
    if len( args ) == 2:
        data_replies = args[0]
        data_in_reply_to = args[1]
    else:
        if len( args ) == 1:
            data_replies = args[0]

    # before query:
    before_query = select(
        [tweets.c.tweet_text, tweets.c.tweet_creation, tweets.c.tweet_userid] ).where( and_(
        tweets.c.tweet_userid == tweet['tweet_userid'], tweets.c.tweet_id < tweet['tweet_id'] ) )
    result_before = conn.execute( before_query.order_by( tweets.c.tweet_id.desc( ) ).limit( 5 ) ).fetchall( )

    # after query:
    after_query = select(
        [tweets.c.tweet_text, tweets.c.tweet_creation, tweets.c.tweet_userid] ).where( and_(
        tweets.c.tweet_userid == tweet['tweet_userid'], tweets.c.tweet_id > tweet['tweet_id'] ) )
    result_after = conn.execute( after_query.order_by( tweets.c.tweet_id.asc( ) ).limit( 5 ) ).fetchall( )

    # after (newer tweets)
    for row in reversed(result_after):
        tweet_after_text = row['tweet_text'].encode('utf-8')
        tweet_after_date = row['tweet_creation']
        tweet_after_text = anonimize_users(tweet_after_text)

        # all_text_after
        print str(tweet_after_date) + ": \t".format(colors.bcolors, colors.bcolors) + str(tweet_after_text)
        #print textwrap.fill(all_text_after)

    # current
    current_tweet_text = tweet['tweet_text'].encode('utf-8')
    current_tweet_author = tweet['tweet_userid']
    current_tweet_date = tweet['tweet_creation']
    current_tweet_text = anonimize_users(current_tweet_text)

    ##### The Tweet and its replies #####
    if tweet_type == 'in_reply_to':
        print_in_reply_to(data_in_reply_to, crawler)

    # The tweet
    # print_bordered_text(current_tweet_text, current_tweet_date)
    string_lst = str(current_tweet_text)
    my_text_frame(string_lst, current_tweet_date)
    print_replies(data_replies, current_tweet_author, crawler)
    ##### ######################### #####

    # before (older tweets)
    for row in result_before:
        tweet_before_text = row['tweet_text'].encode('utf-8')
        tweet_before_date = row['tweet_creation']
        tweet_before_text = anonimize_users( tweet_before_text)
        #all_text_before
        print str(tweet_before_date) + ": \t".format(colors.bcolors, colors.bcolors) + str(tweet_before_text)
        #print textwrap.fill(all_text_before)


def get_key():
    """
    Function to get arrow key pressed
    @return: key type
    """

    try:
        charlist = []
        key = ''
        char = getch.getch( )
        print >> sys.stdout, char

        if char == '\x1b':
            charlist.extend( char )
            for i in range( 2 ):
                sub = getch.getch( )
                charlist.extend( sub )

            for i, j in enumerate( charlist ):
                charlist[i] = unicode( j ).encode( 'ascii' )

            if charlist[2] == 'C':
                key = 'right'
            elif charlist[2] == 'B':
                key = 'down'
            elif charlist[2] == 'D':
                key = 'left'
            elif charlist[2] == 'A':
                key = 'up'

        elif char == 'q':
            key = 'q'
        else:
            key = None
        return key

    except KeyboardInterrupt:
        print >> sys.stdout, 'Goodbye: You pressed Ctrl+C!'


def main():
    # Connect to db
    conn = engine.connect( )

    ANSI_KEYS_TO_STRING = {'up': 'up', 'down': 'down', 'right': 'right', 'left': 'left', 'up': 'up'}

    # Add arguments
    parser = argparse.ArgumentParser( description='Crawl Twitter', prog='groundtruth_reader.py',
                                      usage='%(prog)s [options]' )
    parser.add_argument( '--auth', help='Twitter account for authentication', required=True )

    try:
        args = parser.parse_args( )
    except Exception as e:
        raise e

    ##### Crawler instance #####
    auth = args.auth
    # client_args = {'verify': True}
    crawler = CrawlerTwitter( apikeys=gk(auth))

    ##### Start logic #####
    print_banner( )

    left_key = colored( '(arrow-left)', 'red', attrs=['blink'] )
    right_key = colored( '(arrow-right)', 'red', attrs=['blink'] )
    up_key = colored( '(arrow-up)', 'red', attrs=['blink'] )
    down_key = colored( '(arrow-down)', 'red', attrs=['blink'] )
    quitting = colored( '(q)', 'red', attrs=['blink'] )

    try:
        entered_id = raw_input( )

        ins = reviewers.insert( )
        if not database.checkReviewerId( entered_id ):
            conn.execute( ins, reviewer_id=entered_id )
            print >> sys.stdout, 'New reviewer id saved'
        else:
            print >> sys.stdout, 'Existing reviewer chosen'

        # Subquery for not showing same tweets already annotated to the reviewer
        annotated = select( [gt_tweets.c.fk_tweet_id] ). \
            where( gt_tweets.c.fk_reviewer_id == entered_id ).order_by( gt_tweets.c.fk_tweet_id )

        annotated_count = select( [func.count( )] ).select_from( gt_tweets ).where(
            gt_tweets.c.fk_reviewer_id == entered_id )

        # Query to show how many tweets are annotated by user
        annotated_count_result = conn.execute( annotated_count, reviewer=entered_id )
        for r in annotated_count_result:
            print >> sys.stdout, 'Tweets you have already annotated: ', str( r.values( )[0] )

	    mentions = select( [tweets.c.tweet_id] ).where( and_( tweets.c.msg_type == 'm', tweets.c.depth == 1, tweets.c.retweet is False )).limit(1000)
        # Avoid this join by creating a VIEW out of it
        j = tweets.join( tweet_ranks, mentions.c.tweet_id == tweet_ranks.c.ranked_tweet_id )
        query = select( [tweets] ).select_from( j ).order_by( desc( tweet_ranks.c.rank_tweet ),
                                                             desc( tweet_ranks.c.count_replies ),
                                                             desc( tweet_ranks.c.count_mentions ),
                                                             desc( tweet_ranks.c.count_hashtags ) ). \
           where( tweets.c.tweet_id.notin_( annotated ) )

        result = conn.execute( query, reviewer=entered_id ).fetchall( )

        #### Tweets annotation loop ####
        if len( result ) > 0:
            print >> sys.stdout, 'To quit press key: [q]'
            print >> sys.stdout, "\n"

            for tweet in result:
                if tweet['in_reply_to_tweet_id'] is None:
		    reply_id = None
		else:
		    reply_id = tweet['in_reply_to_tweet_id']

                current_tweet_id = tweet['tweet_id']
                tweet_lang = tweet['tweet_lang']

		if tweet_lang != 'en' or tweet['retweet'] is True or tweet['tweet_text'].startswith( 'RT' ):
                    gt_tweets.update( ).where( gt_tweets.c.fk_tweet_id == current_tweet_id ).values( abusive="hidden" )
                    continue
                else:
                    if reply_id is None:
                        tweet_type = 'normal'

                        # SQL query to get replies to tweet: have in_reply_to_tweet_id = current_tweet_id
                        query_replies = select(
                            [replies.c.tweet_id, replies.c.tweet_text, replies.c.tweet_creation,
                             replies.c.in_reply_to_tweet_id,
                             replies.c.tweet_userid] ).where( replies.c.in_reply_to_tweet_id == current_tweet_id )

                        replies_content = conn.execute( query_replies ).fetchall( )

                        # Check for context
                        get_context( tweet, conn, tweet_type, crawler, replies_content )

                    # It is a In-reply-to, get its original tweet
                    else:
                        tweet_type = 'in_reply_to'
                        query_sources = select(
                            [tweets.c.tweet_id, tweets.c.tweet_text, tweets.c.tweet_creation,
                             tweets.c.in_reply_to_tweet_id,
                             tweets.c.tweet_userid] ).where( tweets.c.tweet_id == reply_id )

                        in_reply_to = conn.execute( query_sources ).fetchone( )

                        # ---- Replies to in_reply_to ---- #

                        # SQL query to get replies to tweet: have in_reply_to_tweet_id = current_tweet_id
                        query_replies = select(
                            [replies.c.tweet_id, replies.c.tweet_text, replies.c.tweet_creation,
                             replies.c.in_reply_to_tweet_id,
                             replies.c.tweet_userid] ).where( replies.c.in_reply_to_tweet_id == current_tweet_id )

                        replies_content = conn.execute( query_replies ).fetchall( )
                        get_context( tweet, conn, tweet_type, crawler, replies_content, in_reply_to )

                # Bar-helper
                print >> sys.stdout, '\n'
                print >> sys.stdout, \
                    '{.BLINK}Abusive{.ENDC}'.format( colors.bcolors, colors.bcolors ) + left_key + \
                    ',{.BLINK}Acceptable{.ENDC}'.format( colors.bcolors, colors.bcolors ) + right_key + \
                    ',{.BLINK}Skip{.ENDC}'.format( colors.bcolors, colors.bcolors ) + down_key + \
                    ',{.BLINK}Undo{.ENDC}'.format( colors.bcolors, colors.bcolors ) + up_key + \
                    ',{.BLINK}Quit{.ENDC}'.format( colors.bcolors, colors.bcolors ) + quitting

                key = get_key( )
                if key == 'q':
                    print >> sys.stdout, 'Goodbye: your pressed quit [q]'
                    sys.exit( 0 )

                while key not in ANSI_KEYS_TO_STRING.itervalues( ):
                    print >> sys.stdout, 'WHAT?'
                    # Bar-helper
                    print >> sys.stdout, '\n'
                    print >> sys.stdout, \
                        '{.BLINK}Abusive{.ENDC}'.format( colors.bcolors, colors.bcolors ) + left_key + \
                        ',{.UNDERLINE}Acceptable{.ENDC}'.format( colors.bcolors, colors.bcolors ) + right_key + \
                        ',{.BLINK}Skip{.ENDC}'.format( colors.bcolors, colors.bcolors ) + down_key + \
                        ',{.BLINK}Undo{.ENDC}'.format( colors.bcolors, colors.bcolors ) + up_key + \
                        ',{.BLINK}Quit{.ENDC}'.format( colors.bcolors, colors.bcolors ) + quitting

                    key = get_key( )

                    if key == 'q':
                        print >> sys.stdout, 'Goodbye: you pressed quit [q]'
                        sys.exit( 0 )

                # Get the cursor
                new_cursor = select( [cursor_gt.c.last_tweet_id] ).where( cursor_gt.c.username == entered_id )
                new_cursor_value = conn.execute( new_cursor, username=entered_id,
                                                 last_tweet_id=tweet['tweet_id'] ).first( )

                # Control input
                if key == ANSI_KEYS_TO_STRING['right']:
                    ins = gt_tweets.insert( )
                    conn.execute( ins, fk_reviewer_id=entered_id, fk_tweet_id=tweet['tweet_id'], abusive='no' )

                    if new_cursor_value is None:
                        insert_cursor = cursor_gt.insert( )
                        conn.execute( insert_cursor, username=entered_id, last_tweet_id=tweet['tweet_id'] )
                    else:
                        update_cursor = cursor_gt.update( ).values( ).where( cursor_gt.c.username == entered_id )
                        conn.execute( update_cursor, username=entered_id, last_tweet_id=tweet['tweet_id'] )

                elif key == ANSI_KEYS_TO_STRING['left']:
                    ins = gt_tweets.insert( )
                    conn.execute( ins, fk_reviewer_id=entered_id, fk_tweet_id=tweet['tweet_id'], abusive='yes' )

                    if new_cursor_value is None:
                        insert_cursor = cursor_gt.insert( )
                        conn.execute( insert_cursor, username=entered_id, last_tweet_id=tweet['tweet_id'] )
                    else:
                        update_cursor = cursor_gt.update( ).values( ).where( cursor_gt.c.username == entered_id )
                        conn.execute( update_cursor, username=entered_id, last_tweet_id=tweet['tweet_id'] )

                elif key == ANSI_KEYS_TO_STRING['up']:

                    user_last_tweet_id = select( [cursor_gt.c.last_tweet_id] ).where(
                        cursor_gt.c.username == entered_id )

                    gt_delete = gt_tweets.delete( ).where(
                        and_( entered_id == gt_tweets.c.fk_reviewer_id,
                              user_last_tweet_id == gt_tweets.c.fk_tweet_id ) )
                    conn.execute( gt_delete, fk_reviewer_id=entered_id, fk_tweet_id=user_last_tweet_id )

                    cursor_gt_delete = cursor_gt.delete( ).where(
                        and_( entered_id == cursor_gt.c.username, user_last_tweet_id == cursor_gt.c.last_tweet_id )
                    )
                    conn.execute( cursor_gt_delete, fk_reviewer_id=entered_id, fk_tweet_id=user_last_tweet_id )

                elif key == ANSI_KEYS_TO_STRING['down']:
                    ins = gt_tweets.insert( )
                    conn.execute( ins, fk_reviewer_id=entered_id, fk_tweet_id=tweet['tweet_id'], abusive='unknown' )

                    if new_cursor_value is None:
                        insert_cursor = cursor_gt.insert( )
                        conn.execute( insert_cursor, username=entered_id, last_tweet_id=tweet['tweet_id'] )
                    else:
                        update_cursor = cursor_gt.update( ).values( ).where( cursor_gt.c.username == entered_id )
                        conn.execute( update_cursor, username=entered_id, last_tweet_id=tweet['tweet_id'] )

                elif key == 'q':
                    print >> sys.stdout, 'Goodbye: your pressed quit [q]'
                    sys.exit( 0 )
                # Clean screen after we have marked the tweet
                cls_next_tweet()

        else:
            print >> sys.stdout, 'Hurray! You have completed all possible tweet annotations'

    except KeyboardInterrupt:
        print >> sys.stdout, 'Goodbye: You pressed Ctrl+C!'
    except Exception:
        traceback.print_exc( file=sys.stdout )
    sys.exit( 0 )


# Main
if __name__ == '__main__':
    main( )

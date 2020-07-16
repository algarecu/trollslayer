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

-- Followers
CREATE OR REPLACE FUNCTION f_followers_count_all_cdf_graph() RETURNS text AS '

sql_all <- paste("select followers_count from t_annotated_tweet_mentions_followers_count");
sql_abusive <- paste("select followers_count from t_annotated_abuse_tweet_mentions_followers_count");
sql_acceptable <- paste("select followers_count from t_annotated_acceptable_tweet_mentions_followers_count");

sql_all_cf <- paste("select followers_count from cf_t_annotated_tweet_mentions_followers_count");
sql_abusive_cf <- paste("select followers_count from cf_t_annotated_abuse_tweet_mentions_followers_count");
sql_acceptable_cf <- paste("select followers_count from cf_t_annotated_acceptable_tweet_mentions_followers_count");

sql_all_ts <- paste("select followers_count from ts_t_annotated_tweet_mentions_followers_count");
sql_abusive_ts <- paste("select followers_count from ts_t_annotated_abuse_tweet_mentions_followers_count");
sql_acceptable_ts <- paste("select followers_count from ts_t_annotated_acceptable_tweet_mentions_followers_count");

################ CF ################
val_all_cf <<- pg.spi.exec(sql_all_cf);
df_all_cf = val_all_cf[,c("followers_count")]
df_all_cf.ordered = sort(df_all_cf)

val_abusive_cf <<- pg.spi.exec(sql_abusive_cf);
df_abusive_cf = val_abusive_cf[,c("followers_count")]
df_abusive_cf.ordered = sort(df_abusive_cf)

val_acceptable_cf <<- pg.spi.exec(sql_acceptable_cf);
df_acceptable_cf = val_acceptable_cf[,c("followers_count")]
df_acceptable_cf.ordered = sort(df_acceptable_cf)

################ TS ################
val_all_ts <<- pg.spi.exec(sql_all_ts);
df_all_ts = val_all_ts[,c("followers_count")]
df_all_ts.ordered = sort(df_all_ts)

val_abusive_ts <<- pg.spi.exec(sql_abusive_ts);
df_abusive_ts = val_abusive_ts[,c("followers_count")]
df_abusive_ts.ordered = sort(df_abusive_ts)

val_acceptable_ts <<- pg.spi.exec(sql_acceptable_ts);
df_acceptable_ts = val_acceptable_ts[,c("followers_count")]
df_acceptable_ts.ordered = sort(df_acceptable_ts)
#####################################

linetype <- c(1:4)
plotchar <- seq(1,3,1)

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/followers-count-all-ccdf-log-axis.pdf'');

plot(sort(df_acceptable_cf), 1-ecdf(df_acceptable_cf)(sort(df_acceptable_cf)), col=aCDFcolor, type="b", xaxt="n", lty=1, lwd=1, pch=22, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of subscribers count in log-log scale")
lines(sort(df_abusive_cf), 1-ecdf(df_abusive_cf)(sort(df_abusive_cf)), col=bCDFcolor, type="b", lty=2, lwd=1, pch=23)

lines(sort(df_acceptable_ts), 1-ecdf(df_acceptable_ts)(sort(df_acceptable_ts)), col=aCDFcolor, type="b", lty=3, lwd=1, pch=24)
lines(sort(df_abusive_ts), 1-ecdf(df_abusive_ts)(sort(df_abusive_ts)), col=bCDFcolor, type="b", lty=4, lwd=1, pch=25)

ticks <- seq(0, 7, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
breaks=c(0, 1, 10, 100, 1000, 10000, 100000, 1000000)
axis(1, at=dput(breaks), labels=labels)

legend("topright", 1:4, cex=0.8, pch=plotchar, lty=linetype, col=c(aCDFcolor,bCDFcolor), bg = "white", legend=c("acceptable cf", "abusive cf", "acceptable ts", "abusive ts"))
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_followers_count_all_cdf_graph();

-- Friends
CREATE OR REPLACE FUNCTION f_followees_count_all_cdf_graph() RETURNS text AS '

sql_all <- paste("select followees_count from t_annotated_tweet_mentions_followees_count");
sql_abusive <- paste("select followees_count from t_annotated_abuse_tweet_mentions_followees_count");
sql_acceptable <- paste("select followees_count from t_annotated_acceptable_tweet_mentions_followees_count");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("followees_count")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("followees_count")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("followees_count")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(followees_count) from t_annotated_tweet_mentions_followees_count;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/followees-count-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable))), col=aCDFcolor, type="b", xaxt="n", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of subscriptions count in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

ticks <- seq(0, 5, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
breaks=c(1, 10, 100, 1000, 10000, 100000)
axis(1, at=dput(breaks), labels=labels)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_followees_count_all_cdf_graph();

-- Mutual Followers
CREATE OR REPLACE FUNCTION f_mutual_followers_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select mutual_followers from t_annotated_all_mutual_followers");
sql_abusive <- paste("select mutual_followers from t_annotated_abusive_mutual_followers");
sql_acceptable <- paste("select mutual_followers from t_annotated_acceptable_mutual_followers");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("mutual_followers")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("mutual_followers")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("mutual_followers")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(mutual_followers) from t_annotated_all_mutual_followers;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/mutual-followers-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable)), log="xy"), col=aCDFcolor, type="s", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of mutual subscribers in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_mutual_followers_all_cdf_graph();

-- Mutual Followees
CREATE OR REPLACE FUNCTION f_mutual_followees_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select mutual_followees from t_annotated_all_mutual_followees");
sql_abusive <- paste("select mutual_followees from t_annotated_abusive_mutual_followees");
sql_acceptable <- paste("select mutual_followees from t_annotated_acceptable_mutual_followees");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("mutual_followees")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("mutual_followees")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("mutual_followees")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(mutual_followees) from t_annotated_all_mutual_followees;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/mutual-followees-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable)), log="xy"), col=aCDFcolor, type="s", xaxt="n", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of mutual subscriptions in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

ticks <- seq(0, 5, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
breaks=c(1, 10, 100, 1000, 10000, 100000)
axis(1, at=dput(breaks), labels=labels)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_mutual_followees_all_cdf_graph();

-- Mutual Followers-Followees
CREATE OR REPLACE FUNCTION f_mutual_followers_followees_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select mutual_followers_followees from t_annotated_all_mutual_followers_followees");
sql_abusive <- paste("select mutual_followers_followees from t_annotated_abusive_mutual_followers_followees");
sql_acceptable <- paste("select mutual_followers_followees from t_annotated_acceptable_mutual_followers_followees");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("mutual_followers_followees")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("mutual_followers_followees")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("mutual_followers_followees")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(mutual_followers_followees) from t_annotated_all_mutual_followers_followees;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/mutual-followers-followees-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable)), log="xy"), col=aCDFcolor, type="s", xaxt="n", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of mutual subscribers-subscriptions in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

ticks <- seq(-3, 3, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
breaks=c(0.1, 1, 10, 100, 1000, 10000, 100000)
axis(1, at=dput(breaks), labels=labels)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_mutual_followers_followees_all_cdf_graph();

-- Mutual Followees-Followers
CREATE OR REPLACE FUNCTION f_mutual_followees_followers_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select mutual_followees_followers from t_annotated_all_mutual_followees_followers");
sql_abusive <- paste("select mutual_followees_followers from t_annotated_abusive_mutual_followees_followers");
sql_acceptable <- paste("select mutual_followees_followers from t_annotated_acceptable_mutual_followees_followers");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("mutual_followees_followers")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("mutual_followees_followers")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("mutual_followees_followers")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(mutual_followees_followers) from t_annotated_all_mutual_followees_followers;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/mutual-followees-followers-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable))), col=aCDFcolor, type="s", xaxt="n", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of mutual subscriptions-subscribers in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

ticks <- seq(0, 5, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
breaks=c(1, 10, 100, 1000, 10000, 100000)
axis(1, at=dput(breaks), labels=labels)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_mutual_followees_followers_all_cdf_graph();

-- Tweet invasive
CREATE OR REPLACE FUNCTION f_tweet_invasive_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select tweet_invasive from t_annotated_all_tweet_invasive");
sql_acceptable <- paste("select tweet_invasive from t_annotated_acceptable_tweet_invasive");
sql_abusive <- paste("select tweet_invasive from t_annotated_abusive_tweet_invasive");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("tweet_invasive")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("tweet_invasive")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("tweet_invasive")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(tweet_invasive) from t_annotated_all_tweet_invasive;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/tweet-invasive-all-ccdf-log-axis.pdf'');

plot(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable)), col=aCDFcolor, log="xy", type="s", lty=2, lwd=3, ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of reciprocal tweet in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_tweet_invasive_all_cdf_graph();

-- Age of account
CREATE OR REPLACE FUNCTION f_age_of_account_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select age_of_account from t_annotated_all_tweets_age_of_account");
sql_acceptable <- paste("select age_of_account from t_annotated_acceptable_tweets_age_of_account");
sql_abusive <- paste("select age_of_account from t_annotated_abusive_tweets_age_of_account");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("age_of_account")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("age_of_account")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("age_of_account")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(age_of_account) from t_annotated_all_tweets_age_of_account;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

pdf(''/tmp/age-of-account-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable)), log="xy"), col=aCDFcolor, type="s", xaxt="n", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of age_of_account in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

ticks <- seq(0, 5, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
breaks=c(1, 10, 100, 1000, 10000, 100000)
axis(1, at=dput(breaks), labels=labels)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_age_of_account_all_cdf_graph();

-- Tweets per day
CREATE OR REPLACE FUNCTION f_tweets_per_day_all_cdf_graph() RETURNS text AS '
sql_all <- paste("select tweets_per_day from t_annotated_all_tweets_per_day");
sql_acceptable <- paste("select tweets_per_day from t_annotated_acceptable_tweets_per_day");
sql_abusive <- paste("select tweets_per_day from t_annotated_abuse_tweets_per_day");

val_all <<- pg.spi.exec(sql_all);
df_all = val_all[,c("tweets_per_day")]
df_all.ordered = sort(df_all)
n = sum(!is.na(df_all))

val_abusive <<- pg.spi.exec(sql_abusive);
df_abusive = val_abusive[,c("tweets_per_day")]
df_abusive.ordered = sort(df_abusive)
n = sum(!is.na(df_abusive))

val_acceptable <<- pg.spi.exec(sql_acceptable);
df_acceptable = val_acceptable[,c("tweets_per_day")]
df_acceptable.ordered = sort(df_acceptable)
n = sum(!is.na(df_acceptable))

df_max <<- pg.spi.exec("select MAX(tweets_per_day) from t_annotated_all_tweets_per_day;");
mymax <- df_max[[1]];

aCDFcolor <- "blue"
bCDFcolor <- "red"

breaks=c(1, 10, 100, 1000, 10000, 100000)

pdf(''/tmp/tweets-per-day-all-ccdf-log-axis.pdf'');

plot(xy.coords(sort(df_acceptable), 1-ecdf(df_acceptable)(sort(df_acceptable)), log="xy"), col=aCDFcolor, type="s", xaxt="n", lty=2, lwd=3, log="xy", ylab="log[P(X > x)]",
	xlab="log(x)", main="CCDF of tweets_per_day in log-log scale")
points(sort(df_abusive), 1-ecdf(df_abusive)(sort(df_abusive)), col=bCDFcolor, type="s", lty=2, lwd=3)

ticks <- seq(0, 5, by=1)
labels <- sapply(ticks, function(i) as.expression(bquote(10^ .(i))))
axis(1, at=dput(breaks), labels=labels)

legend("topright", legend=c("acceptable", "abusive"), lty=2, lwd=3, col=c(aCDFcolor,bCDFcolor), bg = "white")
box()

dev.off();
print(''done'');
'
LANGUAGE plr;
SELECT f_tweets_per_day_all_cdf_graph();

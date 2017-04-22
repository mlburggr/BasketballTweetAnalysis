#!/usr/bin/python
# Python 2.7

# Final Project
# Analyzing Tweet Sentimentality Before Syracuse Men's Basketball Games
# Authors: Maxwell Burggraf and Cristiana Serfass

import sys
sys.path.append("./GetOldTweets")

import twitter
import got
import datetime
import time
import re
import textblob

import config
class BasketballTweetAnalysis:
    # Define class variables.
    # "tweets" is a dictionary that maps each date to a list of tweets.
    # "sentiments" is a dictionary that maps each date to a sum of sentiment values.
    def __init__(self):
        self.tweets = {}
        self.sentiments = {}
        conf = config.Config()
        self.twitterApi = twitter.Twitter(
            auth=twitter.OAuth(conf.access_key,
                               conf.access_secret,
                               conf.consumer_key,
                               conf.consumer_secret)
                            )
    # Gather tweets for a given date range. "gameDate" should be a string in the form:
    # YYYY-MM-DD
    def gatherTweetsForDate(self, gameDate):
        date=datetime.datetime.strptime(gameDate, "%Y-%m-%d").date()

        oneWeekAgo = date - datetime.timedelta(days=7)
        oneDayAgo = date - datetime.timedelta(days=1)

        since = oneWeekAgo.strftime("%Y-%m-%d")
        until = oneDayAgo.strftime("%Y-%m-%d")
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch("Syracuse Basketball").setSince(since).setUntil(until).setMaxTweets(200)

        # Initialize the array of tweets for the gameDate
        self.tweets[gameDate] = []
        
        for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
            geolocation = self.getTweetGeolocationFromId(tweet.id)
            if geolocation != "None":
                self.tweets[gameDate].append(tweet.text)
            else:
                latitude = geolocation["coordinates"][1]
                longitude = geolocation["coordinates"][0]
                if (longitude >= 42.95 and longitude <= 43.15) and (latitude >= -76.3 and latitude <= -75.9):
                    self.tweets[gameDate].append(tweet.text)
        print "Gathered tweets for " + gameDate
        
    def getTweetGeolocationFromId(self, tweetId):
        try:
            geo = self.twitterApi.statuses.show(id=tweetId)["geo"]
        except twitter.api.TwitterHTTPError, e:
            print "Got HTTP error: "
            print e
            print "Waiting 15 minutes"
            time.sleep(60*15 + 5)
            geo = self.twitterApi.statuses.show(id=tweetId)["geo"]
        return geo

    def getSentimentality(self, tweet):
        sentiment = textblob.TextBlob(self.clean_tweet(tweet)).sentiment.polarity

        if sentiment > 0: # Positive sentiment
            return 1
        elif sentiment < 0: # Negative sentiment
            return -1
        else: # Neutral (0) sentiment
            return 0

    # Remove links and special characters from a tweet
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        
    def analyzeTweetSentiments(self):
        if len(self.tweets) == 0:
            print "No tweets gathered!"
            return

        for date in self.tweets:
            distribution = {'pos' : 0, 'neg' : 0, 'neu' : 0}
            self.sentiments[date] = 0
            for tweet in self.tweets[date]:
                sentiment = self.getSentimentality(tweet)
                self.sentiments[date] += sentiment
                if sentiment > 0:  # Positive sentiment
                    distribution['pos'] += 1
                elif sentiment < 0:  # Negative sentiment
                    distribution['neg'] += 1
                else:  # Neutral (0) sentiment
                    distribution['neu'] += 1
            print distribution.items()
        print self.sentiments
        
if __name__ == "__main__":
    b = BasketballTweetAnalysis()
    b.gatherTweetsForDate("2010-12-04")
    b.gatherTweetsForDate("2011-01-01")
    b.gatherTweetsForDate("2011-01-17")
    b.gatherTweetsForDate("2011-02-02")
    b.gatherTweetsForDate("2011-02-09")
    b.gatherTweetsForDate("2011-12-02")
    b.gatherTweetsForDate("2012-01-11")
    b.gatherTweetsForDate("2012-01-16")
    b.gatherTweetsForDate("2012-01-21")
    b.gatherTweetsForDate("2012-02-08")
    b.gatherTweetsForDate("2012-11-25")
    b.gatherTweetsForDate("2012-12-22")
    b.gatherTweetsForDate("2013-01-02")
    b.gatherTweetsForDate("2013-01-26")
    b.gatherTweetsForDate("2013-02-02")
    b.gatherTweetsForDate("2013-11-16")
    b.gatherTweetsForDate("2013-12-28")
    b.gatherTweetsForDate("2014-01-11")
    b.gatherTweetsForDate("2014-02-12")
    b.gatherTweetsForDate("2014-02-22")
    b.gatherTweetsForDate("2014-11-25")
    b.gatherTweetsForDate("2014-12-20")
    b.gatherTweetsForDate("2015-01-17")
    b.gatherTweetsForDate("2015-01-26")
    b.gatherTweetsForDate("2015-02-11")
    b.gatherTweetsForDate("2015-11-26")
    b.gatherTweetsForDate("2015-12-05")
    b.gatherTweetsForDate("2015-12-30")
    b.gatherTweetsForDate("2016-01-13")
    b.gatherTweetsForDate("2016-01-24")
    b.gatherTweetsForDate("2016-11-11")
    b.gatherTweetsForDate("2016-12-05")
    b.gatherTweetsForDate("2016-12-17")
    b.gatherTweetsForDate("2017-01-07")
    b.gatherTweetsForDate("2017-02-04")

    b.analyzeTweetSentiments()

    numTweetsGathered = 0
    for date in b.tweets:
        numTweetsGathered = numTweetsGathered + len(b.tweets[date])
    print str(numTweetsGathered) + " tweets were gathered."
   

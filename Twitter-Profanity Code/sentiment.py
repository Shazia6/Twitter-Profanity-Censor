# Import Files
import os
import sys
import time
import random
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 

class TwitterClient(object):
    def __init__(self):
        consumer_key = 'QIqgjITOfksfMW4lRLDacQ'
        consumer_secret = 'R8x0xN9iSKXGNxUtGKA2hgnlIhh5INZIOdgEfxzk'
        access_token = '1401204486-BeLUAuruh294KeJX8NXvdqjCeZOQcLl6HWmMlgA'
        access_token_secret = 'pwjiLF42TbORaXtkCS5Oc24qywOU0eFN0esVcibA'
 
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        tweets = []
 
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['text'] = self.clean_tweet(parsed_tweet['text'])
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            return tweets
 
        except tweepy.TweepError as e:
            print("Error : " + str(e))
 
if __name__ == "__main__":
    api = TwitterClient()
    tweets = api.get_tweets(query = 'trump', count = 200)
 
    print("Number of Tweets")
    print(len(tweets))

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
    print()
    print("Printing all positive tweets")
    print("\n\nPositive tweets:")
    for tweet in ptweets[:len(ptweets)]:
        print(tweet['text'])
 
    print()
    print("Printing all negative tweets")
    print("\n\nNegative tweets:")
    for tweet in ntweets[:len(ntweets)]:
        print(tweet['text'])


    from profanity import profanity


    print()
    print()
    new_filtered_positive = []
    new_filtered_negative = []
    module_pos_off_count=0
    module_pos_noff_count=0
    module_neg_off_count=0
    module_neg_noff_count=0
    custom_pos_off_count=0
    custom_pos_noff_count=0
    custom_neg_off_count=0
    custom_neg_noff_count=0
    t_count = 1

    for tweet in ptweets:
        t_check = tweet["text"]


        t = profanity.censor(tweet["text"])
        if (t_check != t):
        	module_pos_off_count= module_pos_off_count+1
        	print("Module Positive Tweet Number : "+str(t_count)+" is Offensive")
        else:
        	module_pos_noff_count = module_pos_noff_count+1
        	print("Module Positive Tweet Number : "+str(t_count)+" is Non-Offensive")
        t_count += 1



        new_filtered_positive.append(t)


    t_count = 1
    print()
    print()

    for tweet in ntweets:
        t_check = tweet["text"]
        t = profanity.censor(tweet["text"]) 
        new_filtered_negative.append(t)

        if (t_check  != t):
        	module_neg_off_count=module_neg_off_count+1
        	print("Module Negative Tweet Number : "+str(t_count)+" is Offensive")
        else:
        	module_neg_noff_count=module_neg_noff_count+1
        	print("Module Negative Tweet Number : "+str(t_count)+" is Non-Offensive")
        t_count += 1

    print()
    print("Printing all positive filtered tweets")
    print("\n\nPositive tweets:")
    for tweet in new_filtered_positive[:len(ptweets)]:
        print(tweet)
 
    print()
    print("Printing all negative filtered tweets")
    print("\n\nNegative tweets:")
    for tweet in new_filtered_negative[:len(ntweets)]:
        print(tweet)


    print()
    print("End of module filter")
    print()
    print()
    print()

    # Checking for swear words

    swear_words_file = open("badwords-google.txt", "r")
    swear_words_data = swear_words_file.read()
    swear_words = swear_words_data.split()

    #print(swear_words)

    # "My, my! Hello my friendly mystery".replace("my", "")


    t_count = 1

    new_filtered_positive = []
    new_filtered_negative = []
    for tweet in ptweets:
        t_check = tweet["text"]
        t = tweet["text"]
        word_list = t.split();
        filtered = ' '.join([i for i in word_list if i.lower() not in swear_words])



        if(t != filtered):
        	custom_pos_off_count=custom_pos_off_count+1
        	print("Custom Positive Tweet Number : "+str(t_count)+" is Offensive")            
        else:
        	custom_pos_noff_count=custom_pos_noff_count+1
        	print("Custom Positive Tweet Number : "+str(t_count)+" is Non-Offensive")
        t_count +=1
        new_filtered_positive.append(filtered)

    print()
    print()
    t_count = 1
    for tweet in ntweets:
        t_check = tweet["text"]
        t = tweet["text"]
        word_list = t.split();
        filtered = ' '.join([i for i in word_list if i.lower() not in swear_words])

        if(t != filtered):
        	custom_neg_off_count=custom_neg_off_count+1
        	print("Custom Negative Tweet Number : "+str(t_count)+" is Offensive")            
        else:
        	custom_neg_noff_count=custom_neg_noff_count+1
        	print("Custom Negative Tweet Number : "+str(t_count)+" is Non-Offensive")
        t_count+=1
        new_filtered_negative.append(filtered)

    print()
    print("Printing all positive filtered tweets")
    print("\n\nPositive tweets:")
    for tweet in new_filtered_positive[:len(ptweets)]:
        print(tweet)
 
    print()
    print("Printing all negative filtered tweets")
    print("\n\nNegative tweets:")

    for tweet in new_filtered_negative[:len(ntweets)]:
        print(tweet)
    
    module_pos_off_perc = module_pos_off_count/len(ptweets)
    module_pos_off_perc = module_pos_off_perc*100

    module_pos_noff_perc = module_pos_noff_count/len(ptweets)
    module_pos_noff_perc = module_pos_noff_perc*100

    module_neg_off_perc = module_neg_off_count/len(ntweets)
    module_neg_off_perc = module_neg_off_perc*100

    module_neg_noff_perc = module_neg_noff_count/len(ntweets)
    module_neg_noff_perc = module_neg_noff_perc*100

    custom_pos_off_perc = custom_pos_off_count/len(ptweets)
    custom_pos_off_perc = custom_pos_off_perc*100

    custom_pos_noff_perc = custom_pos_noff_count/len(ptweets)
    custom_pos_noff_perc = custom_pos_noff_perc*100

    custom_neg_off_perc = custom_neg_off_count/len(ntweets)
    custom_neg_off_perc = custom_neg_off_perc*100

    custom_neg_noff_perc = custom_neg_noff_count/len(ntweets)
    custom_neg_noff_perc = custom_neg_noff_perc*100

    print("MODULE PERCENTAGE")

    print("percentage of offensive tweets in positive statements")
    print(module_pos_off_perc)
    print("percentage of non-offensive tweets in positive statements")
    print(module_pos_noff_perc)
    print("percentage of offensive tweets in negative statements")
    print(module_neg_off_perc)
    print("percentage of non-offensive tweets in negative statements")
    print(module_neg_noff_perc)

    print("CUSTOM PERCENTAGE")

    print("percentage of offensive tweets in positive statements")
    print(custom_pos_off_perc)
    print("percentage of non-offensive tweets in positive statements")
    print(custom_pos_noff_perc)
    print("percentage of offensive tweets in negateive statements")
    print(custom_neg_off_perc)
    print("percentage of non-offensive tweets in negative statements")
    print(custom_neg_noff_perc)
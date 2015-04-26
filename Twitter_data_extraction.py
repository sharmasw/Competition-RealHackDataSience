import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data_path = 'D:/Project Data/Twitter_data/twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)

tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

tweets

tweets.to_csv('D:/Project Data/Twitter_data/rawdata.csv', encoding='utf-8')
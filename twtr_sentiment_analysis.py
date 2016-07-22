from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json


#consumer key, consumer secret, access token, access secret.
ckey="<client key>"
csecret="<client secret>"
atoken="<access token>"
asecret="<access secret>"

class listener(StreamListener):

    def on_data(self, data):
        try:
            all_data = json.loads(data)

            tweet = all_data["text"].encode('utf-8')
            sid = SentimentIntensityAnalyzer()
            sentiment_value = sid.polarity_scores(tweet)['compound']
            print sentiment_value
            if float(sentiment_value) < 0.0:
                sentiment = "neg"
            elif float(sentiment_value) >= 0.0:
                sentiment = "pos"
            print tweet, sentiment, sentiment_value

            if abs(sentiment_value) > 0.1:
                output = open("twitter-out.txt","a")
                output.write(sentiment)
                output.write('\n')
                output.close()

            return True
        except Exception as e:
            print e
            pass

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["<keywords>"])

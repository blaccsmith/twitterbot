import json
import tweepy
import asyncio
from time import sleep
from constants import CONSTANTS
from profanity_check import predict

class TweepyClient(tweepy.Stream):

    auth = tweepy.OAuthHandler(CONSTANTS['Consumer_Key'], CONSTANTS['Consumer_Secret'], CONSTANTS['Access_Key'], CONSTANTS['Access_Secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, loop, send_to_channel, **kwargs):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret, **kwargs)
        self.send_to_channel = send_to_channel
        self.loop = loop

    def on_status(self, tweet):
        tweetInfo = json.loads(json.dumps(tweet._json))

        tweetText = tweetInfo['text']
        reply_to_status_id = tweetInfo['in_reply_to_status_id_str']

        # Only mentions and coding channels ex. @blaccxyz_ #coding-resources
        if "@blaccxyz_" in tweetText:
            if len(tweetText.split()) > 2:
                print("Only mentions with available discord channel allowed ex. @blaccxyz_ #coding-resources") 
                return

            self.send_message([tweetText, reply_to_status_id])
            return

        if self.is_invalid_tweet(tweetInfo):
            return
        
        # Like the tweet
        if not tweet.favorited:
            try:
                self.api.create_favorite(id=tweetInfo['id'])
            except Exception as e:
                print("Error liking tweet because: " + str(e))

        ## Retweet the tweet
        if not tweet.retweeted:
            try:
                self.api.retweet(id=tweetInfo['id'])
            except Exception as e:
                print("Error retweeting tweet because: " + str(e))

    def send_message(self, textData):
        future = asyncio.run_coroutine_threadsafe(self.send_to_channel(textData), self.loop)
        try:
            future.result(5)
        except Exception as e:
            print('Error: %s' % e)

    def on_error(self, status):
        if status == 420:
            print("Error detected: " + str(status) + "\nClosing and reconnecting the Stream...")
            # Wait 15 min before reconnecting
            sleep(900)
            return False
        else:
            print("Error detected: " + str(status))

    def is_invalid_tweet(self, tweetInfo):
        ## Guard clause for retwets
        if 'retweeted_status' in tweetInfo or tweetInfo['is_quote_status']:
            return True
        
        # ## Guard clause for possibly sensitive tweets
        if 'possibly_sensitive' in tweetInfo and tweetInfo['possibly_sensitive']:
            return True

        ## Guard clause for tweets with more than 3 hashtags
        if len(tweetInfo['entities']['hashtags']) > 3:
            print("Tweet with more than 3 hashtags detected. Ignoring...")
            return True
        ## Guard clause for extended tweets with more than 5 hashtags
        if 'extended_tweet' in tweetInfo and len(tweetInfo['extended_tweet']['entities']['hashtags']) > 5:
            print("Extended tweet with more than 5 hashtags detected. Ignoring...")
            return True

        predict_score = predict([tweetInfo['text']])

        if predict_score:
            message = 'Detected a sensitive tweet here: https://twitter.com/twitter/statuses/' + str(tweetInfo['id_str'])
            self.api.send_direct_message(recipient_id=CONSTANTS['moderator_id'], text=message)
            return True

        return False
import tweepy
import time
import MySQLdb
from keys import api
from keys import db
from random import randint

print('Bot is online...')

### CONNECTING THE DATABASE ###
db = MySQLdb.connect(
    host = db.host, 
    user = db.user, 
    passwd = db.passwd, 
    db = db.db
)

### SELECT ALL THE COMPLIMENTS FROM DATABASE ###
cursor = db.cursor()
cursor.execute("SELECT * FROM compliments")
compliments = cursor.fetchall()
db.close()

### CONNECTING THE TWITTER API ###
auth = tweepy.OAuthHandler(api.CONSUMER_KEY, api.CONSUMER_SECRET)
auth.set_access_token(api.ACCESS_KEY, api.ACCESS_SECRET)
api = tweepy.API(
    auth, 
    wait_on_rate_limit = True, 
    wait_on_rate_limit_notify = True
)

### GETTING SOME USEFUL VARIABLES ###
bot = api.me()
FILE_NAME = "last_seen_id.txt"

### FUNCTION TO GET THE ID OF THE LAST MENTION TWEET ###
def retrive_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

### FUNCTION TO STORE THE ID OF THE LAST MENTION TWEET ###
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

### FUNCTION TO LIKE THE TWEET WITH MENTION ###
def like_tweet(id):
    api.create_favorite(id)

### FUNCTION TO CHOOSE ONE RANDOM COMPLIMENT ###
def pick_random_compliment():
    number = randint(0, len(compliments) - 1)
    return compliments[number][1]

### FUNCTION TO REPLY ALL THE TWEETS ###
def reply_to_tweets():
    last_seen_id = retrive_last_seen_id(FILE_NAME)

    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended'
    )

    for mention in reversed(mentions):
        if bot.screen_name in mention.full_text:
            print("Mantion made by @" + mention.user.screen_name)
            print("Mantion text: " + mention.full_text)
            print("Answering...")
            last_seen_id = mention.id
            store_last_seen_id(last_seen_id, FILE_NAME)

            like_tweet(mention.id)
            api.update_status(
                status = pick_random_compliment(), 
                in_reply_to_status_id = str(mention.id), 
                auto_populate_reply_metadata = True
            )

### LOOP THAT MAKES SCRIPT RUNNING ###
while True:
    reply_to_tweets()
    time.sleep(12)
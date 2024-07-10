import tweepy
import os
import random
from datetime import datetime
import shutil  # Import the shutil module for file operations

api_key = ''
api_secret = ''
access_token = ''
access_token_secret = ''
media_path = r"folder path with all the images you want to use"
allImages = list()
log = r"wherever you want to save the .txt that logs what you post"
now = datetime.now()
used_media_path = r"folder path for the images that were used alread"

# print("started at ", now.strftime("%d/%m/%Y %H:%M:%S"))
def chooseRandomImage(path=media_path):
    nr = 0
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]

    for img in files:
        allImages.append(img)
    choice = random.randint(0, len(allImages) - 1)
    return os.path.join(path, allImages[choice])


def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get Twitter connection using OAuth1.0"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get Twitter connection using OAuth2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)

img_path = chooseRandomImage()
media = client_v1.media_upload(filename=img_path)
media_id = media.media_id

client_v2.create_tweet(media_ids=[media_id])

shutil.move(img_path, os.path.join(used_media_path, os.path.basename(img_path)))



with open(log, 'a') as log_img:
    log_img.write(img_path[16:] + ' ' + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')

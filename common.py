import logging
import datetime

import tweepy # pip install tweepy
import pymysql # pip install PyMySQL

import credentials

def get_logger(name, path=""):
    # see https://docs.python.org/3/howto/logging-cookbook.html
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(path + '%s.log' % name)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def get_db(credentials):
    # see https://pymysql.readthedocs.io/en/latest/modules/connections.html
    db = pymysql.connect(host=credentials.database['host'], 
                         user=credentials.database['user'], 
                         password=credentials.database['password'], 
                         db=credentials.database['database'],
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor,
                         autocommit=True)
    cursor = db.cursor()
    return db, cursor

def get_twitter_api(credentials, stream_type):
    # see http://docs.tweepy.org/en/3.7.0/auth_tutorial.html
    auth = tweepy.OAuthHandler(credentials.twitter_api[stream_type]['consumer_key'], \
                               credentials.twitter_api[stream_type]['consumer_secret'])
    auth.set_access_token(credentials.twitter_api[stream_type]['access_token'], \
                          credentials.twitter_api[stream_type]['access_token_secret'])
    api = tweepy.API(auth)
    return api

def now_timestamp():
    return datetime.datetime.utcnow().strftime(r'%Y-%m-%d %H:%M:%S')
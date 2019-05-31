from flask import Flask, render_template, request, jsonify, Response
import os
from os import path, stat
import pickle
import hashlib
import json
import time
from functools import wraps
  
import pymysql

import credentials
import logging
import datetime

import tweepy # pip install tweepy
import pymysql # pip install PyMySQL

from flask_gzip import Gzip

import credentials

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

gzip = Gzip(app)

def get_database():
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

def now_timestamp():
    return datetime.datetime.utcnow().strftime(r'%Y-%m-%d %H:%M:%S')

def file_timestamp():
    return datetime.datetime.utcnow().strftime(r'%Y%m%d%H')

def make_response(response, errors=[], elapsed_time=0):
    return jsonify({'response': response, 'errors': errors, 'elapsed_time': elapsed_time})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v2/topics/')
def get_topics():
    db, cursor = get_database()
    start_time = time.time()
    cursor.execute("SELECT id, name FROM t_topics ORDER BY name ASC")
    rows = cursor.fetchall()
    db.close()
    elapsed_time = time.time() - start_time
    return make_response(rows, elapsed_time=elapsed_time), 200
    
@app.route('/api/v2/topic/<int:topic_id>/statuses/')
def get_topic_statuses(topic_id):
    start_time = time.time()
    db, cursor = get_database()
    
    # try to use cache first
    cached_file = '/var/www/luluview/cache/statuses_%03d_%s.pkl' % (int(topic_id), file_timestamp())
    if path.exists(cached_file):
        age_seconds = time.time() - os.stat(cached_file).st_mtime
        if age_seconds < 30:
            rows = pickle.load(open(cached_file, 'rb'))
            elapsed_time = time.time() - start_time
            response = make_response(rows, elapsed_time=elapsed_time)
            db.close()
            return response, 200
                
    cursor.execute(("SELECT s.id, s.text, s.retweet_count, s.favorite_count, s.lang, s.entities, "
                    "s.user_id, s.created_at, s.updated_at, u.name, u.screen_name, "
                    "u.followers_count, u.profile_image_url_https, u.follow "
                    "FROM t_statuses s INNER JOIN t_status_topic st ON s.id = st.status_id "
                    "LEFT JOIN t_users u ON s.user_id = u.id "
                    "WHERE st.topic_id=%s "
                    "AND s.created_at > DATE_SUB(NOW(), INTERVAL 7 day) "
                    "ORDER BY s.updated_at DESC"), topic_id)
    
    rows = cursor.fetchall()
    for row in rows:
        entities_dict = json.loads(row['entities'])
        row['entities'] = {'urls': entities_dict['urls']} if entities_dict else dict()
        
    pickle.dump(rows, open(cached_file, 'wb'))
    elapsed_time = time.time() - start_time
    response = make_response(rows, elapsed_time=elapsed_time)
    db.close()
    return response, 200

@app.route('/api/v2/topic/<int:topic_id>/users/')
def get_topic_users(topic_id):
    start_time = time.time()
    db, cursor = get_database()
    
    # try to use cache first
    cached_file = '/var/www/luluview/cache/users_%03d_%s.pkl' % (int(topic_id), file_timestamp())
    if path.exists(cached_file):
        age_seconds = time.time() - os.stat(cached_file).st_mtime
        if age_seconds < 30:
            rows = pickle.load(open(cached_file, 'rb'))
            elapsed_time = time.time() - start_time
            response = make_response(rows, elapsed_time=elapsed_time)
            db.close()
            return response, 200
                
    cursor.execute(("SELECT u.*, COUNT(s.id) AS count_statuses, SUM(s.retweet_count) + SUM(s.favorite_count) AS shares "
                    "FROM t_statuses s INNER JOIN t_status_topic st ON s.id = st.status_id "
                    "INNER JOIN t_users u ON s.user_id = u.id "
                    "WHERE st.topic_id=%s "
                    "AND s.created_at > DATE_SUB(NOW(), INTERVAL 7 day) "
                    "GROUP BY u.id "
                    "ORDER BY shares DESC"), topic_id)
    rows = cursor.fetchall()
    for row in rows:
        row['shares'] = int(row['shares'])
    pickle.dump(rows, open(cached_file, 'wb'))
    elapsed_time = time.time() - start_time
    response = make_response(rows, elapsed_time=elapsed_time)
    db.close()
    return response, 200
    
@app.route('/api/v2/topic/<int:topic_id>/urls/')
def get_topic_opengraph(topic_id):
    start_time = time.time()
    db, cursor = get_database()
    
    # try to use cache first
    cached_file = '/var/www/luluview/cache/urls_%03d_%s.pkl' % (int(topic_id), file_timestamp())
    if path.exists(cached_file):
        age_seconds = time.time() - os.stat(cached_file).st_mtime
        if age_seconds < 30:
            rows = pickle.load(open(cached_file, 'rb'))
            elapsed_time = time.time() - start_time
            response = make_response(rows, elapsed_time=elapsed_time)
            db.close()
            return response, 200
                
    cursor.execute(("SELECT u.url, u.display_url, u.opengraph_json AS opengraph, "
                    "COUNT(s.id) AS count_statuses, SUM(s.retweet_count) + SUM(s.favorite_count) AS shares "
                    "FROM t_statuses s INNER JOIN t_status_topic st ON s.id = st.status_id "
                    "INNER JOIN t_status_urls su ON su.status_id = s.id "
                    "INNER JOIN t_urls u ON su.url = u.url "
                    "WHERE st.topic_id=%s "
                    "AND s.created_at > DATE_SUB(NOW(), INTERVAL 7 day) "
                    "GROUP BY u.url "
                    "ORDER BY shares DESC"), topic_id)
    
    rows = cursor.fetchall()
    for row in rows:
        opengraph_dict = json.loads(row['opengraph'])
        row['opengraph'] = opengraph_dict if opengraph_dict else dict()
        row['shares'] = int(row['shares'])
        
    pickle.dump(rows, open(cached_file, 'wb'))
    elapsed_time = time.time() - start_time
    response = make_response(rows, elapsed_time=elapsed_time)
    db.close()
    return response, 200

if __name__ == "__main__":
    
    app.run()

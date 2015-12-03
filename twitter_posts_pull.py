# -*- coding: utf-8 -*-

import base64
import requests
import datetime
import time
from time import mktime
import os
import csv
## file contains keys for authentication
from twitter_key1 import consumer_key,consumer_secret

## returns json with results of pull
def twitterpull(username,count,max_id):
    params = {"screen_name": username,
              "count": count,
              "include_rts": "true",
              "exclude_replies": "false",
              "max_id":max_id
                }
    header = {"Authorization": "Bearer {}".format(bearer_token),
              'Accept-Encoding': 'gzip', }
    r = requests.get(base_url + endpoint,
                         params=params,
                         headers=header)
    return r.json

#######################
### Enter handles here:

companies = []

### Enter date to pull back to:

#######################

date_limiter = time.strptime('2015-11-01', '%Y-%m-%d')
date_limiter = datetime.datetime.fromtimestamp(mktime(date_limiter))

base_url = 'https://api.twitter.com/1.1/'
endpoint = 'statuses/user_timeline.json'

userhome = os.path.expanduser('~')
text_file = input('Enter the filename with single-quotes (no extension needed): ')
newfile = userhome + text_file + '.txt'


print "Getting token..."
bearer_token_credentials = base64.urlsafe_b64encode(
    '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')).decode('ascii')
url = 'https://api.twitter.com/oauth2/token'
headers = {
    'Authorization': 'Basic {}'.format(bearer_token_credentials),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
}
data = 'grant_type=client_credentials'
response = requests.post(url, headers=headers, data=data)
response_data = response.json()
if response_data['token_type'] == 'bearer':
    bearer_token = response_data['access_token']
else:
    raise RuntimeError('unexpected token type: {}'.format(response_data['token_type']))

x = 1

print "Starting user pull..."
for user in companies:
    ## This part gets the ID of the most recent tweet
    print "Pulling " + user
    max_id = ''
    check_date = datetime.datetime.now()
    prelim_result = twitterpull(user,1,'')
    for tweet in r.json():
        max_id = prelim_result
    ## This part pulls older tweets
    while check_date > date_limiter:
        full_results = twitterpull(user,200,max_id - 1)
        for tweet in full_results:
            date = tweet["created_at"]
            clean_date = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date, '%a %b %d %H:%M:%S +0000 %Y'))
            check_date = datetime.datetime.strptime(clean_date,'%Y-%m-%d %H:%M:%S')
            if check_date >= date_limiter:
                write_me = []
                max_id = tweet['id_str']
                id = tweet['id_str']
                content = tweet["text"]
                clean_content = content.encode('ascii','ignore')
                cleanest_content = clean_content.replace('\n',' ').replace('\r',' ').replace('\t',' ')
                link = 'https://twitter.com/' + user + '/status/' + id
                retweets = tweet["retweet_count"]
                favorites = tweet["favorite_count"]
                write_me.extend((user,link,cleanest_content,str(clean_date),str(retweets),str(favorites)))
                output_writer = csv.writer(newfile, delimiter="\t")
                output_writer.writerows(write_me)
        ### You can only do 180 calls within 15 minutes. This puts the thread to sleep for 15 minutes if you hit 170 calls.
        if x % 170 == 0:
            x+=1
            time.sleep(900)
            continue
        else:
            x+=1

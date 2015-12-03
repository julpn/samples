# -*- coding: utf-8 -*-

from contextlib import closing
from creds import db
import datetime
import logging
import time

LOG_FILENAME = 'error_log.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

def convert_date(str):
    date = str[:10]
    time = str[11:19]
    dt = date + time
    f = '%Y-%m-%d%H:%M:%S'
    return datetime.datetime.strptime(dt, f)
    
def check_for_key(json, key):
    if json:
        if key in json:
            return json[key]
    else:
        return ''

def clean(string):
    if str(string) == '[]':
        return
    else:
        return string

def handle_array(json,key):
    if json:
        array = check_for_key(json,key)
        return clean(array)
    else:
        return
    
class tag_handler:
    def __init__(self,dict):
        self.client_list = ''
        self.topic_list = ''
        clist = []
        tlist = []
        for cthing in dict['matching_rules']:
            if cthing is not None and cthing['tag'] is not None:
                tag = cthing['tag'].split(';')
                for subtag in tag:
                    subtag = subtag.strip()
                    if subtag[:2].lower() == 'c:' and subtag not in clist:
                        clist.append(subtag)
                    if subtag[:2].lower() == 't:' and subtag not in tlist:
                        tlist.append(subtag)
        self.client_list = ",".join(clist)
        self.topic_list = ",".join(tlist)

class get_fields:
    def __init__(self,dict):
        self.post_id = check_for_key(dict,'id')
        self.author_name = check_for_key(dict['actor'],'displayName')
        self.author_username = check_for_key(dict['actor'],'preferredUsername')
        self.author_link = check_for_key(dict['actor'],'link')
        self.author_created = convert_date(check_for_key(dict['actor'],'postedTime'))
        self.author_profile_image = check_for_key(dict['actor'],'image')
        self.author_personal_url = check_for_key(dict['actor']['links'],'href')
        self.author_followers = check_for_key(dict['actor'],'followersCount')
        self.author_following = check_for_key(dict['actor'],'friendsCount')
        self.author_lists_count = check_for_key(dict['actor'],'listedCount')
        self.author_statuses_count = check_for_key(dict['actor'],'statusesCount')
        self.author_time_zone = check_for_key(dict['actor'],'twitterTimeZone')
        self.author_verified = check_for_key(dict['actor'],'verified')
        self.author_bio = check_for_key(dict['actor'],'summary')
        self.author_languages = str(handle_array(dict['actor'],'languages'))
        self.author_favorites_count = check_for_key(dict['actor'],'favoritesCount')
        location_obj = check_for_key(dict['actor'],'location')
        self.author_location = check_for_key(location_obj,'displayName')
        self.post_action = check_for_key(dict,'verb')
        self.post_type = 'twitter'
        self.post_date = convert_date(check_for_key(dict,'postedTime'))
        self.post_source = check_for_key(dict['generator'],'displayName')
        self.post_link = check_for_key(dict,'link')
        self.post_content = check_for_key(dict,'body')
        self.post_favorites_count = check_for_key(dict,'favoritesCount')
        self.post_hashtags = str(handle_array(dict['twitter_entities'],'hashtags'))
        self.post_trends = str(handle_array(dict['twitter_entities'],'trends'))
        self.post_urls = str(handle_array(dict['twitter_entities'],'urls'))
        self.post_mentions = str(handle_array(dict['twitter_entities'],'user_mentions'))
        self.post_symbols = str(handle_array(dict['twitter_entities'],'symbols'))
        urls = check_for_key(dict['twitter_entities'],'media')
        self.media_urls = []
        if urls:
            for item in urls:
                facts = (item['media_url'],item['type'])
                media_obj = ':'.join(facts)
                self.media_urls.append(media_obj)
        self.media_urls = str(self.media_urls)
        self.post_retweet_count = check_for_key(dict,'retweetCount')
        self.post_language = check_for_key(dict,'twitter_lang')
        post_tags = handle_array(dict,'gnip')
        all_tags = tag_handler(post_tags)
        self.client_tags = all_tags.client_list
        self.topic_tags = all_tags.topic_list
        location_data = check_for_key(dict['gnip'],'profileLocations')
        if location_data:
            for item in location_data:
                coordinates = check_for_key(item['geo'],'coordinates')
                self.long = str(coordinates[0])
                self.lat = str(coordinates[1])
        else:
            self.lat = ''
            self.long = ''


    def insert_time(self):
        try:
            with closing(db.cursor()) as cur:
                cur.execute("""
                insert ignore into gnip.twitter (post_id,
                author_name,
                author_username,
                author_link,
                author_created,
                author_profile_image,
                author_personal_url,
                author_followers,
                author_following,
                author_lists_count,
                author_statuses_count,
                author_time_zone,
                author_verified,
                author_languages,
                author_favorites_count,
                post_type,
                post_date,
                post_source,
                post_link,
                post_content,
                post_favorites_count,
                post_hashtags,
                post_trends,
                post_urls,
                post_mentions,
                post_symbols,
                media_urls,
                post_retweet_count,
                post_language,
                post_tags,
                post_clients,
                author_location,
                author_bio,
                post_channel,
                post_lat,
                post_long )

                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,(self.post_id,
                self.author_name,
                self.author_username,
                self.author_link,
                self.author_created,
                self.author_profile_image,
                self.author_personal_url,
                self.author_followers,
                self.author_following,
                self.author_lists_count,
                self.author_statuses_count,
                self.author_time_zone,
                self.author_verified,
                self.author_languages,
                self.author_favorites_count,
                self.post_type,
                self.post_date,
                self.post_source,
                self.post_link,
                self.post_content,
                self.post_favorites_count,
                self.post_hashtags,
                self.post_trends,
                self.post_urls,
                self.post_mentions,
                self.post_symbols,
                self.media_urls,
                self.post_retweet_count,
                self.post_language,
                self.topic_tags,
                self.client_tags,
                self.author_location,
                self.author_bio,
                self.post_action,
                self.lat,
                self.long
                )
                            )
                db.commit()
        except MySQLdb.Error, e:
            logging.error(datetime.datetime.now(),'SQL Error: ' + e)
            time.sleep(60)
            continue

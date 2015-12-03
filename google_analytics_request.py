from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http
from apiclient.discovery import build
import json
from datetime import datetime, timedelta
from contextlib import closing
from creds import db

client_email = my_client_email
type = 'Channel'

for num in range(1,61):
    day = datetime.today() - timedelta(days=num)
    date = str(day.strftime('%Y-%m-%d'))
    private_key_path = myprivatekey
    with open(private_key_path) as f:
        private_key = f.read()
    credentials = SignedJwtAssertionCredentials(client_email, private_key,
                                                'https://www.googleapis.com/auth/analytics.readonly')
    http_auth = credentials.authorize(Http())
    service = build('analytics', 'v3', http=http_auth)
    response = service.data().ga().get(
        ids='ga:xxxxxxxx',
        start_date=date,
        end_date=date,
        metrics='ga:pageviews,ga:sessionDuration,ga:pageviewsPerSession,ga:bounces,ga:sessions',
        dimensions='ga:channelGrouping',  # sort='-ga:visits',  #filters='ga:medium==organic',  #start_index='1',
        max_results='25').execute()

    json_str = json.dumps(response)
    json_dict = json.loads(json_str)

    data = json_dict['rows']
    for record in data:
        channel = record[0]
        page_views = record[1]
        avg_session_dur = record[2]
        views_per_session = record[3]
        bounces = record[4]
        sessions = record[5]

        with closing(db.cursor()) as cur:
            cur.execute("""
			insert ignore into database.table (date, channel,type, page_views, bounces, avg_session_dur, views_per_session,sessions)
			values (%s,%s,%s,%s,%s,%s,%s,%s)
			on duplicate key update page_views = %s, bounces = %s, 
			avg_session_dur = %s, views_per_session = %s, sessions = %s
			""", (
            date, channel, type, page_views, bounces, avg_session_dur, views_per_session, sessions, page_views, bounces,
            avg_session_dur, views_per_session, sessions))
            db.commit()

import urllib2
from lxml.html import fromstring
from contextlib import closing
from creds import db

## List of Pinterest users
brands = []
for user in brands:
    url = 'http://www.pinterest.com/' + user
    response = urllib2.urlopen(url)
    text = response.read()
    doc = fromstring(text)
    with closing(db.cursor()) as cur:
        for pin in doc.find_class('Module Pin summary'):
            for repin_count in pin.find_class('socialMetaCount repinCountSmall'):
                if repin_count.text is None:
                    pins = '0'
                else:
                    pins = int(repin_count.text.replace('\n', ''))

                ### LIKES
            for like_count in pin.find_class('socialMetaCount likeCountSmall'):
                if like_count.text is None:
                    likes = '0'
                else:
                    likes = int(like_count.text.replace('\n', ''))

                ### LINKS
            for link_raw in pin.find_class('pinImageWrapper'):
                link = 'http://www.pinterest.com' + link_raw.get('href')

            ### PIN DESCRIPTION
            if not pin.find_class('pinDescription'):
                description = ''
            else:
                for pin_name in pin.find_class('pinDescription'):
                    description = (pin_name.text.replace('\n', '')).replace('More', '')
                    description = description.lstrip()

                ### COMMETNTS
            if not pin.find_class('socialMetaCount commentCountSmall'):
                comments = 0
            else:
                for with_comments in pin.find_class('socialMetaCount commentCountSmall'):
                    comments = int(with_comments.text.replace('\n', ''))
            cur.execute("""
            insert ignore into sodelicious.pinterest_pins (company, pin_name,link,repins,likes,comments,board_name)
            values (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE
            repins = %s, likes = %s, comments = %s
            """, (description, link, pins, likes, comments,pins, likes, comments))
            db.commit()

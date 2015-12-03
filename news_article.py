from creds import db
from newspaper import Article
from contextlib import closing

with closing(db.cursor()) as cur:
    cur.execute("""
    select url, id,headline from database.table
    where url != '' and url is not null and scraped_content is null
    order by id
    """)
    rows = cur.fetchall()
    for article in rows:
        url = article[0]
        lang = 'en'
        int_id = article[1]
        headline = article[2]
        print str(int_id)
        try:
            print "getting article..."
            article_get = Article(url=url, language=lang)
            print "downloading..."
            article_get.download()
            print "parsing..."
            article_get.parse()
            print "setting scraped content..."
            scraped_content = article_get.text
            print "importing data..."
            cur.execute(
                """
            update database.table
            set scraped_content = %s where headline = %s and scraped_content is null
            """,(scraped_content,headline))
            print "committing..."
            db.commit()

        except:
            print "got error with " + url + " which is " + lang

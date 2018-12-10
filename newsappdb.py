# Database code for News Reporting Tool

import psycopg2, bleach

DBNAME = "news"

def get_articles():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select title, time from articles order by time desc")
  posts = c.fetchall()
  db.close()
  return posts

def add_article(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("insert into articles values (%s)", (bleach.clean(content),))  # good
  # db.commit()
  db.close()


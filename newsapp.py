#!/usr/bin/env python3
# 
# A web service to expose the news database.

from flask import Flask, request, redirect, url_for

import psycopg2

app = Flask(__name__)

# HTML template for the reporting tool page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>News Reporting Tool</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      hr.postbound { width: 50%%; }
    </style>
  </head>
  <body>
    <h1>News Database Reporting Tool</h1>
    <h3>The answers to udaciously important questions about news DB.</h3>
    <!-- report content will go here -->
%s
  </body>
</html>
'''

# HTML template for listing items
REPORT = '''\
    <table><tr>
    <td>%s</td><td> -- </td><td>%s views</td>
    </tr></table>
'''

REPORT2 = '''\
    <div>%s -- %s percent error</div>
'''

def get_topArticles():
  """Return top three articles from news."""
  db = psycopg2.connect(database="news")
  c = db.cursor()
  c.execute("select title, total from top3articles")  
  posts = c.fetchall()
  db.close()
  return posts

def get_popularAuthors():
  """Return all authors sorted by popularity."""
  db = psycopg2.connect(database="news")
  c = db.cursor()
  c.execute("select name, total from authorsbypopularity")
  posts = c.fetchall()
  db.close()
  return posts

def get_topDateError():
  """Return the top date on which more than 1% of requests led to errors."""
  db = psycopg2.connect(database="news")
  c = db.cursor()
  c.execute("select TO_CHAR(date :: DATE, 'Mon dd, yyyy'), error from topdateinerror")
  posts = c.fetchall()
  db.close()
  return posts

@app.route('/', methods=['GET'])
def main():
  '''Main page of the reporting tool.'''
  posts = "<b>1. What are the most popular three articles of all time?</b>"
  posts += "".join(REPORT % (x, y) for x, y in get_topArticles())
  posts += "<br><hr><b>2. Who are the most popular article authors of all time?</b>"
  posts += "".join(REPORT % (x, y) for x, y in get_popularAuthors())
  posts += "<br><hr><b>3. On which days did more than 1% of requests lead to errors?</b>"
  posts += "".join(REPORT2 % (x, y) for x, y in get_topDateError())
  html = HTML_WRAP % posts
  return html


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)

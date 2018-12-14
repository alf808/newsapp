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

try:
    db = psycopg2.connect(database="news")
    c = db.cursor()
except:
    print ("Unable to connect to the database")


def get_topArticles():
    """Return top three articles from news."""
    c.execute("select title, total from top3articles")
    posts = c.fetchall()
    return posts


def get_popularAuthors():
    """Return all authors sorted by popularity."""
    c.execute("select name, total from authorsbypopularity")
    posts = c.fetchall()
    return posts


def get_topDateError():
    """Return the dates on which more than 1% of requests led to errors."""
    c.execute(
        "select TO_CHAR(date::DATE,'Mon dd, yyyy'),error from topdateinerror"
        )
    posts = c.fetchall()
    return posts


@app.route('/', methods=['GET'])
def main():
    '''Main page of the reporting tool.'''
    posts = "<b>1. What are the most popular three articles of all time?</b>"
    posts += "".join(REPORT % (x, y) for x, y in get_topArticles())
    posts += "<br><hr><b>2. Who are the most popular authors of all time?</b>"
    posts += "".join(REPORT % (x, y) for x, y in get_popularAuthors())
    posts += "<br><hr><b>3. What days led to more 1% of error requests?</b>"
    posts += "".join(REPORT2 % (x, y) for x, y in get_topDateError())
    html = HTML_WRAP % posts
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

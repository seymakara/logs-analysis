#! /usr/bin/env python
import psycopg2

DBNAME = "news"


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except:
        print("<error message>")


def popular_articles():
    """Print the most popular 3 articles
    from the 'database'."""
    db, c = connect()
    query = """SELECT title,count(*) AS num
    FROM log, articles
    WHERE log.path = '/article/' || articles.slug
    GROUP BY 1 ORDER BY num DESC
    LIMIT 3;"""
    c.execute(query)
    results = c.fetchall()
    print "---THE ANSWER OF THE 1ST QUESTION---"
    for result in results:
        print result[0], result[1], 'views'
    db.close()


def popular_authors():
    """Print the most popular
    authors from the 'database'."""
    db, c = connect()
    query = """SELECT authors.name,top_author_ids.views
  FROM (
      SELECT articles.author AS id, count(*) AS views
      FROM log, articles
      WHERE log.path = '/article/' || articles.slug
      GROUP BY 1
      ORDER BY views DESC
    ) top_author_ids
  JOIN authors
  ON top_author_ids.id = authors.id;"""
    c.execute(query)
    results = c.fetchall()
    print "---THE ANSWER OF THE 2ND QUESTION---"
    for result in results:
        print result[0], result[1], 'views'
    db.close()


def days_with_errors():
    """Print the days with errors
    more than %1 of requests from the 'database'."""
    db, c = connect()
    query = """SELECT all_table.day,
    CAST(errors_table.errors AS FLOAT) /
    CAST (all_table.requests AS FLOAT) * 100
  FROM (
      SELECT date_trunc('day', time) AS day, count(1) AS errors
      FROM log
      WHERE status LIKE '%404%'
      GROUP BY 1
    ) errors_table
  JOIN (
      SELECT date_trunc('day', time) AS day,
      count(1) AS requests
      FROM log GROUP BY 1
    ) all_table
  ON errors_table.day = all_table.day
  WHERE CAST (errors_table.errors AS FLOAT) /
  CAST (all_table.requests AS FLOAT) > 0.01;"""
    c.execute(query)
    results = c.fetchall()
    print "---THE ANSWER OF THE 3RD QUESTION---"
    for result in results:
        print result[0].date(), round(result[1], 2), '%', 'errors'
    db.close()


if __name__ == "__main__":
    popular_articles()
    popular_authors()
    days_with_errors()

## Synopsis

This code will connect to that database which includes the data about the articles, authors and the log of a newspaper. The code also will use SQL queries to analyze the  data, and print out the answers to some questions.

## Code Example
`import psycopg2` is necessary to connect to the database

`DBNAME = "news"` News is the name of the database.

The code below connects to the news database
`def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except:
        print("<error message>")`

The code below executes the sql code to bring three most popular article read.
    `def popular_articles():
        """Print the most popular 3 articles
        from the 'database'."""
        db, c = connect()
        query = """SELECT title,count(*) AS num
        FROM log, articles
        WHERE log.path = '/article/' || articles.slug
        GROUP BY 1 ORDER BY num DESC
        LIMIT 3;"""
        c.execute(query)`

The code below prints the results in an order.
    `results = c.fetchall()
      print "---THE ANSWER OF THE 1ST QUESTION---"
      for result in results:
          print result[0], result[1], 'views'
      db.close()`

## Motivation
 This project is a requirement to finish Backend Development.

## Installation

Download the sql_project zip file.

Requirement: You need to have psql database up and running on your terminal.

1) Create a database with `createdb news`
2) Run `newsdata.sql` to create tables and insert data.
3) Then run my code `python sql_project.py`.

## Tests

Access the file on your favorite terminal.
Run this command `python sql_project.py` on the terminal.

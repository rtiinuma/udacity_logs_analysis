#!/usr/bin/env python3
import db

try:
    # Attempt connection to news database
    newsdb = db.Database("news")

    # Question 1 - most popular articles:
    # Query uses toparticles view to get count of each article.
    # View uses regular expression extraction for article slug.
    # Joined with the articles table to get the full title.
    # Inner join to ignore views without articles
    q1 = "\nQuestion 1: What are the most popular three articles of all time?"
    print(q1)
    pop_articles_q = """
        SELECT title as Title, cnt as Views
        FROM toparticles
        INNER JOIN articles
        ON slug = article
        ORDER BY Views DESC
        LIMIT 3;"""
    pop_articles = newsdb.select_query(pop_articles_q)

    # Print articles and view count
    if pop_articles is not None:
        print("\tArticle \t- \tViews")
        for article in pop_articles:
            print('"{}" \t- \t{}'.format(article[0].title(), str(article[1])))
    else:
        print("No results.")

    # Question 2 - most popular authors:
    # Query uses view to get count of each article.
    # View uses regular expression extraction for article slug.
    # Joins with articles table to get author id
    # Joins with authors table to get author name
    # Inner join to ignore views without articles or authors
    q2 = "\nQuestion 2: Who are the most popular article authors of all time?"
    print(q2)
    pop_authors_q = """
        SELECT  authors.name, SUM(cnt)
        FROM toparticles
        INNER JOIN articles
        ON slug = article
        INNER JOIN authors
        ON articles.author = authors.id
        GROUP BY authors.name
        ORDER BY SUM(cnt) DESC;"""
    pop_authors = newsdb.select_query(pop_authors_q)

    # Print authors and view count
    if pop_authors is not None:
        print("\tAuthor \t- \tViews")
        for author in pop_authors:
            print('{} \t- \t{}'.format(author[0].title(), str(author[1])))
    else:
        print("No results.")

    # Question 3 - dates with most errors
    # Uses subquery to select date, number of errors, and total hits
    # Counts error as any request that did not return 2XX response
    # Calculates error percentage amd selects days with > 1%
    q3 = ("\nQuestion 3: On which days did more than "
          "1% of requests lead to errors?")
    print(q3)
    errors_q = """
        SELECT TO_CHAR(dt, 'FMMonth DD, YYYY'),
        TO_CHAR((errors::float / total * 100), 'FM999.00') as error_prcnt
        FROM(
        SELECT DATE(time) as dt,
        SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END) as errors,
        count(status) as total
        FROM log
        GROUP BY DATE(time)
        ) counts
        WHERE (errors::float / total * 100) > 1; """
    errors = newsdb.select_query(errors_q)

    # Print date and error percentage
    if errors is not None:
        print("\tDate \t- \tErrors")
        for error in errors:
            print('{} \t- \t{}%'.format(error[0].title(), str(error[1])))
    else:
        print("No results.")

except Exception as e:
    # Display error if anything went wrong
    print(str(e))

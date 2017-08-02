
import datetime, psycopg2, db

try:
    # Attempt connection to news database
    newsdb = db.Database("news")

    '''Question 1 - most popular articles:
       Query uses subquery to select count of each article.
       Subquery uses regular expression extraction for article slug.
       Results are joined with the articles table to get the full title.'''
    pop_articles_q = """ SELECT title as Title, cnt as Views
    FROM articles
    INNER JOIN
    (SELECT substring(path from '%/article/#"%#"' for '#') as article, COUNT(path) as cnt
     FROM log 
     WHERE path LIKE '%/article/%' 
     GROUP BY path 
    ) log
    ON slug = log.article
    LIMIT 3;"""

    print("\nQuestion 1: What are the most popular three articles of all time?")
    pop_articles = newsdb.select_query(pop_articles_q)
    if pop_articles is not None:
        print("\tArticle \t- \tViews")
        for article in pop_articles:
            print('"{}" \t- \t{}'.format(article[0].title(),str(article[1])))
    else:
        print("No results.")

    '''Question 2 - most popular authors:
       Query uses subquery to
       '''
    pop_authors_q = """ SELECT  authors.name, SUM(cnt)
    FROM articles
    INNER JOIN
    (SELECT substring(path from '%/article/#"%#"' for '#') as art, COUNT(path) as cnt
     FROM log 
     WHERE path LIKE '%/article/%' 
     GROUP BY path 
    ) art_log
    ON slug = art
    INNER JOIN authors
    ON articles.author = authors.id
    GROUP BY authors.name
    ORDER BY SUM(cnt) DESC;"""

    print ("\nQuestion 2: Who are the most popular article authors of all time?")
    pop_authors = newsdb.select_query(pop_authors_q)
    if pop_authors is not None:
        print("\tAuthor \t- \tViews")
        for author in pop_authors:
            print('{} \t- \t{}'.format(author[0].title(),str(author[1])))
    else:
        print("No results.")

    # question 3 - dates with most errors
    errors_q = """ SELECT TO_CHAR(dt, 'FMMonth DD, YYYY'), TO_CHAR((errors::float / total * 100), 'FM999.00') as error_prcnt
    FROM(
     SELECT DATE(time) as dt, SUM(CASE WHEN status NOT LIKE '2%' THEN 1 ELSE 0 END) as errors, count(status) as total
     FROM log 
     GROUP BY DATE(time)
    ) counts
    where (errors::float / total * 100) > 1; """

    print("\nQuestion 3: On which days did more than 1% of requests lead to errors?")
    errors = newsdb.select_query(errors_q)
    if errors is not None:
        print("\tDate \t- \tErrors")
        for error in errors:
            print('{} \t- \t{}%'.format(error[0].title(),str(error[1])))
    else:
        print("No results.")

except Exception as e:
    print(str(e))
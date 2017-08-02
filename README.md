# Project: Logs Analysis

Submission for "Project: Logs Analysis" for Udacity Full-Stack Program.

Author: Renee Iinuma

Date: 8/2/2017

## Project Questions
1. **What are the most popular three articles of all time?** Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.
2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. **On which days did more than 1% of requests lead to errors?** The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

## To Run

- Ensure **Python3** (Developed with Python 3.5.2) is installed
- Ensure `news` database exists with the following tables:
  * `articles`
  * `authors`
  * `log`
- Create `toparticle` view
``` 
CREATE VIEW toparticles AS 
 SELECT substring(path from '%/article/#"%#"' for '#') as article, COUNT(path) as cnt
 FROM log 
 WHERE path LIKE '%/article/%' 
 GROUP BY path;
```
- Run `python3 analysis.py`
- Program queries `news` database to answer each question
- Program will print results to the console

## Output
- Example project output is located in `output.txt`
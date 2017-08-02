#!/usr/bin/env python3
import psycopg2


class Database():
    '''Database class to encapsulated connections and queries to database. '''
    def __init__(self, dbname):
        '''Database class constructor initializing database name and
        validating connection. Throws exception if connection to specified
        database is not valid.'''
        try:
            db = psycopg2.connect("dbname="+dbname)
            db.close()
            self.dbname = dbname
        except psycopg2.DatabaseError as e:
            raise Exception("Error connecting to specified db {} -- "
                            .format(dbname)+str(e))

    def select_query(self, query):
        '''Database class function to run specified elect query and
           return result. Query will access database specified
           in constructor.'''
        try:
            db = psycopg2.connect("dbname="+self.dbname)
            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            db.close()
            return rows
        except Exception as e:
            print("Error querying database -- " + str(e))

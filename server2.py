from flask import Flask, send_file, request, Response
from flask_cors import CORS

from config import config

import psycopg2
import http.client
import json
 
BASE_URL = 'api.themoviedb.org'
API_KEY = 'ef3a8359454d45c5a58ad9e6dc9913e7'

def trial():
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        #try to insert a movie
        SQL = "INSERT INTO movies (title,year,type) VALUES(%s,%s,%s);"
        data = ("Hannibal",2001,"Mistery")
        cur.execute(SQL,data)

        #eliminate a movie
        #SQL = "DELETE FROM movies WHERE title = 'Hannibal' "
        #cur.execute(SQL)

        #query to get all from movies
        print("Querying all movies' content")
        SQL = "SELECT * FROM movies"
        cur.execute(SQL)
        movs = cur.fetchall()
        print(movs)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.commit()
            conn.close()
            print('Database connection closed.')

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return "Done"


def request(method, pathname):
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = "{}"
    headers = {'content-type': 'application/json;charset=utf-8'}
    conn.request(method, '{}api_key={}'.format(pathname, API_KEY), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')


def getconnection():
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return conn

def search_movies_by_query(query):
    return request('GET', '/3/search/movie?query={}&'.format(query))


def get_movie(movie_title):
    conn = getconnection()
    cur = conn.cursor()

    SQL = "SELECT TOP(1) FROM movies WHERE title=%s"
    cur.execute(SQL,movie_title)

    movie = cur.fetchone()

    movie = request('GET', '/3/movie/{}?'.format(movie_id))
    movie = json.loads(movie)

    #add new movie to database
    try:
     # movies.insert_one(movie)
      print('The movie is added to the database')
    except BaseException as e:
      print('Couldn not insert data to the dabase. Response from API: ' + str(movie) + '    ' + str(e))

  
    print('Movie is in the database')

 
 
if __name__ == '__main__':
    trial()
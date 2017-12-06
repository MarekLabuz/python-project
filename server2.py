from flask import Flask, send_file, request, Response
from flask_cors import CORS

from config import config

import psycopg2
import http.client
import json
 
BASE_URL = 'api.themoviedb.org'
API_KEY = 'ef3a8359454d45c5a58ad9e6dc9913e7'

#API
def request(method, pathname):
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = "{}"
    headers = {'content-type': 'application/json;charset=utf-8'}
    conn.request(method, '{}api_key={}'.format(pathname, API_KEY), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')

#DATABASE
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

#connecting to the database
conn = getconnection()
cur = conn.cursor() 


def search_movies_by_query(query):
    return request('GET', '/3/search/movie?query={}&'.format(query))

def add_movie_to_DB(movie_id):   
    movie = request('GET', '/3/movie/{}?'.format(movie_id))
    movie = json.loads(movie)

    credits = request('GET', '/3/movie/{}/credits?'.format(movie_id))
    credits = json.loads(credits)

    director_id = ''

    for attr in credits['crew']:
        if attr['job'] == 'Director':
            director_id = attr['id']

    #add movie to database
    SQL_insert_movie = "INSERT INTO movies (id, title, year, rating, director, length, description, poster_thumb) VALUES ({}, '{}', '{}', {},'{}', {}, '{}', '{}');".format(movie["id"], movie["title"], movie["release_date"], movie["vote_average"], director_id, movie["runtime"], movie["overview"], movie["poster_path"])
    cur.execute(SQL_insert_movie)

    #add genres
    SQL_insert_genres = "INSERT INTO genres (movie_id, genre) VALUES ({}, '{}');"
    for attr in movie['genres']:
        cur.execute(SQL_insert_genres.format(movie["id"], attr["name"]))


    #add people connected with the movie to the database:

    #director
    if person_not_exists(director_id):
        add_person_to_DB(director_id)
        add_movie_person(movie["id"], director_id, "Director")

    #cast
    for actor in credits['cast']:
        actor_id = actor['id']
        if person_not_exists(actor_id):
            add_person_to_DB(actor_id)
            add_movie_person(movie_id, actor_id, actor['character'])


def person_not_exists(director_id):
    SQL_select_person_by_id =  "SELECT * FROM people WHERE id={} LIMIT 1;".format(director_id)
    cur.execute(SQL_select_person_by_id)
    person = cur.fetchone();
    return False if person else True

def add_person_to_DB(person_id):
    person = request('GET', '/3/person/{}?'.format(person_id))
    person = json.loads(person)

    SQL_insert_person = "INSERT INTO people (id, name, popularity, birthday, place_of_birth, gender) VALUES ({}, '{}', {}, '{}', '{}', {});".format(person["id"], person["name"], person["popularity"], 
        person["birthday"], person["place_of_birth"], person["gender"])
    cur.execute(SQL_insert_person)
    
def add_movie_person(movie_id, person_id, role):
    SQL_insert_movie_person = "INSERT INTO movie_person (movie_id, person_id, role_name) VALUES ({}, {}, '{}');".format(movie_id, person_id, role)
    cur.execute(SQL_insert_movie_person)



def get_movie(movie_id):
    SQL_select_movie_by_id = "SELECT * FROM movies WHERE id={} LIMIT 1;".format(movie_id)
    cur.execute(SQL_select_movie_by_id)

    movie = cur.fetchone()

    if movie:
        print("movie in database")
        return movie
    else:
        print("adding movie, actors...")
        add_movie_to_DB(movie_id)

        conn.commit();
        cur.execute(SQL_select_movie_by_id)
        movie_details = cur.fetchone()
        return movie_details

def get_actor(actor_id):
    SQL_select_person_by_id = "SELECT * FROM people WHERE id={} LIMIT 1;".format(actor_id)
    cur.execute(SQL_select_person_by_id)

    actor = cur.fetchone()
    
    if actor:
        print("actor in database")
        return actor
    else:
        print("adding actor...")
        add_person_to_DB(actor_id)
        conn.commit();

        cur.execute(SQL_select_person_by_id)
        actor_details = cur.fetchone()        
        return actor_details
 
if __name__ == '__main__':
    get_movie(11457)
    get_actor(2454)
    #closing connection
    cur.close()
from config import config

import psycopg2
import http.client
import json
import urllib.parse
import threading
import logging 

BASE_URL = 'api.themoviedb.org'
API_KEY = 'ef3a8359454d45c5a58ad9e6dc9913e7'

logging.basicConfig(level=logging.DEBUG)

movies_columns = ["id", "title", "year", "rating", "director", "length", "description", "poster_thumb"]
actors_columns = ["id", "name", "popularity", "birthday", "place_of_birth", "gender"]


def create_dictionary(t, columns):
    return {column: t[i] for i, column in enumerate(columns)}


def r(text=''):
    if text is None:
        return ''
    return text.replace('\'', '')


# API
def request(method, pathname):
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = "{}"
    headers = {'content-type': 'application/json;charset=utf-8'}
    conn.request(method, '{}api_key={}'.format(pathname, API_KEY), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')


# DATABASE
def getconnection():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        logging.debug(error)
    finally:
        return conn

# connecting to the database
conn = getconnection()
cur = conn.cursor()


def search_movies_by_person(person_id):
    return request('GET', '/3/person/{}/movie_credits?'.format(person_id))


def search_movies_by_query(query):
    return request('GET', '/3/search/movie?query={}&'.format(urllib.parse.quote(query)))


def add_movie_to_db(movie_id, by_actor_id):
    movie = request('GET', '/3/movie/{}?'.format(movie_id))
    movie = json.loads(movie)

    credits = request('GET', '/3/movie/{}/credits?'.format(movie_id))
    credits = json.loads(credits)

    director_id = ''

    for attr in credits['crew']:
        if attr['job'] == 'Director':
            director_id = attr['id']

    # add movie to database
    sql_insert_movie = "INSERT INTO movies (id, title, year, rating, director, length, description, poster_thumb) VALUES ({}, '{}', '{}', {},'{}', {}, '{}', '{}');".format(movie["id"], r(movie.get("title", "")), movie["release_date"], movie["vote_average"], director_id, movie["runtime"], r(movie.get("overview", "")), movie["poster_path"])
    cur.execute(sql_insert_movie)
    conn.commit()
    logging.debug('Movie inserted.')

    queries_genres = []
    # add genres
    sql_insert_genres = "INSERT INTO genres (movie_id, genre) VALUES ({}, '{}');"
    for attr in movie['genres']:
       queries_genres.append(sql_insert_genres.format(movie["id"], attr["name"]))
    runParallel(queries_genres)
    logging.debug('Genres inserted.')

    # ---------add people connected with the movie to the database:---------

    # director
    if person_not_exist(director_id):
        cur.execute(add_person_to_db(director_id))
        cur.execute(add_movie_person(movie["id"], director_id, "Director"))
        logging.debug('Director inserted.')

    # cast
    i = 0
    if by_actor_id != '':
        by_actor = list(filter(lambda a: a['id'] == int(by_actor_id), credits['cast']))
        if len(by_actor) > 0:
            cur.execute(add_movie_person(movie_id, by_actor_id, by_actor[0]['character']))

    queries_person = []
    queries_movie_person = []

    for actor in credits['cast']:
        if i == 5:
            break
        if by_actor_id == '' or int(by_actor_id) != actor['id']:
            i += 1
            actor_id = actor['id']
            if person_not_exist(actor_id):
                queries_person.append(add_person_to_db(actor_id))
            queries_movie_person.append(add_movie_person(movie_id, actor_id, actor['character']))
    runParallel(queries_person)
    runParallel(queries_movie_person)      

def runParallel(queries):
    threads = []
    for q in queries:
        t = threading.Thread(target=runQuery, args=(q,))
        threads.append(t)
        t.start()
        logging.debug("Thread: " + q)

def runQuery(query):
    cur.execute(query)
    conn.commit()

def person_not_exist(director_id):
    sql_select_person_by_id = "SELECT * FROM people WHERE id={} LIMIT 1;".format(director_id)
    cur.execute(sql_select_person_by_id)
    person = cur.fetchone()
    return False if person else True


def add_person_to_db(person_id):
    person = request('GET', '/3/person/{}?'.format(person_id))
    person = json.loads(person)

    sql_insert_person = "INSERT INTO people (id, name, popularity, birthday, place_of_birth, gender) VALUES ({}, '{}', {}, '{}', '{}', {});".format(person["id"], r(person.get("name", "")), person.get("popularity", 0), person.get("birthday", ""), r(person.get("place_of_birth", "")), person["gender"])
    # cur.execute(sql_insert_person)
    return sql_insert_person

def add_movie_person(movie_id, person_id, role):
    sql_insert_movie_person = "INSERT INTO movie_person (movie_id, person_id, role_name) VALUES ({}, {}, '{}');".format(movie_id, person_id, r(role))
    # cur.execute(sql_insert_movie_person)
    return sql_insert_movie_person

def get_movie(movie_id, actor_id):
    sql_select_movie_by_id = "SELECT * FROM movies WHERE id={} LIMIT 1;".format(movie_id)
    cur.execute(sql_select_movie_by_id)

    movie = cur.fetchone()

    if not movie:
        logging.debug("adding movie, actors...")
        add_movie_to_db(movie_id, actor_id)

        conn.commit()
        cur.execute(sql_select_movie_by_id)
        movie = cur.fetchone()
    else:
        logging.debug("movie already in the database")

    movie = create_dictionary(movie, movies_columns)

    sql_select_people_by_movie = "SELECT id, name FROM (SELECT * FROM movie_person WHERE movie_id = {}) AS iq JOIN people ON person_id = id;".format(movie_id)
    cur.execute(sql_select_people_by_movie)

    people = cur.fetchall()

    people = [create_dictionary(person, ["id", "name"]) for person in people]

    movie["people"] = people

    return movie


def get_actor(actor_id):
    sql_select_person_by_id = "SELECT * FROM people WHERE id={} LIMIT 1;".format(actor_id)
    cur.execute(sql_select_person_by_id)

    actor = cur.fetchone()
    
    if actor:
        logging.debug("actor in the database")
        return create_dictionary(actor, actors_columns)
    else:
        logging.debug("adding actor...")
        add_person_to_db(actor_id)
        conn.commit()

        cur.execute(sql_select_person_by_id)
        actor_details = cur.fetchone()        
        return create_dictionary(actor_details, actors_columns)
 
# if __name__ == '__main__':
#     get_movie(1492, '')
#     get_actor(2454)
#     # closing connection
#     cur.close()
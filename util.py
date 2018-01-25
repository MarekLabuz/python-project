from config import config
import psycopg2, psycopg2.extras
import http.client
import json
import urllib.parse
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


def search_movies_by_genre(genre_id):
    return request('GET', '/3/discover/movie?sort_by=popularity.desc&page=1&with_genres={}&'.format(genre_id))


def search_movies_by_keyword(keyword_id):
    return request('GET', '/3/keyword/{}/movies?sort_by=popularity.desc&page=1&'.format(keyword_id))


def add_movie_to_db(movie_id, by_actor_id, by_keyword_id):
    movie = request('GET', '/3/movie/{}?'.format(movie_id))
    movie = json.loads(movie)

    credits = request('GET', '/3/movie/{}/credits?'.format(movie_id))
    credits = json.loads(credits)

    keywords = request('GET', '/3/movie/{}/keywords?'.format(movie_id))
    keywords = json.loads(keywords)["keywords"]

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
    for attr in movie['genres']:
       queries_genres.append({"movie_id": movie["id"], "id":attr["id"],"genre":attr["name"]})
    psycopg2.extras.execute_batch(cur, "INSERT INTO genres (movie_id, id, genre) VALUES (%(movie_id)s, %(id)s, %(genre)s);", queries_genres)
    logging.debug('Genres inserted.')

    # ---------add people connected with the movie to the database:---------

    # director
    if director_id != '' and person_not_exist(director_id):
        cur.execute("INSERT INTO people (id, name, popularity, birthday, place_of_birth, gender) VALUES (%(id)s, %(name)s, %(popularity)s, %(birthday)s, %(place_of_birth)s, %(gender)s)", get_person(director_id))
        cur.execute("INSERT INTO movie_person (movie_id, person_id, role_name) VALUES({}, {}, '{}');".format(movie["id"], director_id, "Director"))

    if by_actor_id is None:
        by_actor_id = ''

    # cast
    i = 0
    if by_actor_id != '':
        by_actor = list(filter(lambda a: a['id'] == int(by_actor_id), credits['cast']))
        if len(by_actor) > 0:
            cur.execute("INSERT INTO movie_person (movie_id, person_id, role_name) VALUES({}, {}, '{}');".format(movie_id, by_actor_id, r(by_actor[0]['character'])))

    queries_person = []
    queries_movie_person = []

    for actor in credits['cast']:
        if i == 5:
            break
        if by_actor_id == '' or int(by_actor_id) != actor['id']:
            i += 1
            actor_id = actor['id']
            if person_not_exist(actor_id):
                queries_person.append(get_person(actor_id))
            queries_movie_person.append({"movie_id":movie_id, "person_id":actor_id, "role_name":r(actor['character'])})

    psycopg2.extras.execute_batch(cur, "INSERT INTO people (id, name, popularity, birthday, place_of_birth, gender) VALUES (%(id)s, %(name)s, %(popularity)s, %(birthday)s, %(place_of_birth)s, %(gender)s)", queries_person)
    psycopg2.extras.execute_batch(cur, "INSERT INTO movie_person (movie_id, person_id, role_name) VALUES (%(movie_id)s, %(person_id)s, %(role_name)s)", queries_movie_person)
    logging.debug('Actors inserted.')

    if by_keyword_id is None:
        by_keyword_id = ''

    if by_keyword_id != '':
        by_keyword = list(filter(lambda k: k['id'] == int(by_keyword_id), keywords))
        if len(by_keyword) > 0:
            cur.execute("INSERT INTO keywords (movie_id, id, keyword) VALUES ({}, {}, '{}');".format(movie_id, by_keyword_id, by_keyword[0]["name"]))

    j = 0
    queries_keywords = []
    for attr in keywords:
        if j == 7:
            break
        if by_keyword_id == '' or int(by_keyword_id) != attr["id"]:
            j += 1
            keyword_id = attr["id"]
            if keyword_not_exist(keyword_id):
                queries_keywords.append({"movie_id": movie["id"], "id":keyword_id,"keyword":attr["name"]})

    psycopg2.extras.execute_batch(cur, "INSERT INTO keywords (movie_id, id, keyword) VALUES (%(movie_id)s, %(id)s, %(keyword)s);", queries_keywords)
    logging.debug('Keywords inserted.')


def runQuery(query):
    cur.execute(query)
    conn.commit()

def person_not_exist(director_id):
    sql_select_person_by_id = "SELECT * FROM people WHERE id={} LIMIT 1;".format(director_id)
    cur.execute(sql_select_person_by_id)
    person = cur.fetchone()
    return False if person else True

def keyword_not_exist(keyword_id):
    sql_select_keyword_by_id = "SELECT * FROM keywords WHERE id={} LIMIT 1;".format(keyword_id)
    cur.execute(sql_select_keyword_by_id)
    keyword = cur.fetchone()
    return False if keyword else True

def get_person(person_id):
    person = request('GET', '/3/person/{}?'.format(person_id))
    person = json.loads(person)
    ins_pers = {"id":int(person["id"]), "name":r(person.get("name", "")), "popularity":float(person.get("popularity", 0)), "birthday":person.get("birthday", ""), "place_of_birth":r(person.get("place_of_birth", "")), "gender":int(person["gender"])}
    return ins_pers

def get_movie(movie_id, actor_id, keyword_id):
    sql_select_movie_by_id = "SELECT * FROM movies WHERE id={} LIMIT 1;".format(movie_id)
    cur.execute(sql_select_movie_by_id)

    movie = cur.fetchone()

    if not movie:
        logging.debug("adding movie, actors...")
        add_movie_to_db(movie_id, actor_id, keyword_id)

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

    sql_select_genres_by_movie = "SELECT id, genre as name FROM genres WHERE movie_id = {}".format(movie_id)
    cur.execute(sql_select_genres_by_movie)
    genres = cur.fetchall()
    movie["genres"] = [create_dictionary(genre, ["id", "name"]) for genre in genres]

    sql_select_keywords_by_movie = "SELECT id, keyword as name FROM keywords WHERE movie_id = {}".format(movie_id)
    cur.execute(sql_select_keywords_by_movie)
    keywords = cur.fetchall()
    movie["keywords"] = [create_dictionary(keyword, ["id", "name"]) for keyword in keywords]

    logging.debug(movie)
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
#     get_movie(83819, '')
#     get_actor(2454)
#     # closing connection
#     cur.close()
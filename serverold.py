from flask import Flask, send_file, request, Response, make_response
from flask_cors import CORS


import http.client
import json

app = Flask(__name__)
CORS(app)


BASE_URL = 'theimdbapi.org'


@app.route('/')
def root():
    return send_file('./front/build/index.html', mimetype='text/html')


def requestMovie(method, pathname):
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = "{}"
    headers = {'content-type': 'application/json;charset=utf-8'}
    conn.request(method, pathname, payload, headers)
    response = conn.getresponse()
    content = response.read().decode('utf-8')
    response = make_response(content)
    response.headers['content-type'] = 'application/json'
    diz = json.loads(content)

    for d in diz:
        title = d['title']
        year = d['year']
        rating = d['rating']
        director = d['director']
        genre = d['genre'][0]
        character00 = d['cast'][0]['name']
        character01 = d['cast'][1]['name']
        character02 = d['cast'][2]['name']
        character03 = d['cast'][3]['name']
        character04 = d['cast'][4]['name']
        character05 = d['cast'][5]['name']
        character06 = d['cast'][6]['name']
        character07 = d['cast'][7]['name']
        character08 = d['cast'][8]['name']
        character09 = d['cast'][9]['name']
        break

    return response

def requestActor(method, pathname):
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = "{}"
    headers = {'content-type': 'application/json;charset=utf-8'}
    conn.request(method, pathname, payload, headers)
    response = conn.getresponse()
    content = response.read().decode('utf-8')
    response = make_response(content)
    response.headers['content-type'] = 'application/json'
    diz = json.loads(content)

    for d in diz:
        name = d['title']
        birthday = d['birthday']
        birthplace = d['birthplace']
        image_link = d['image']['thumb']
        break

    return response


def search_movies(title,year):
    return requestMovie('GET', '/api/find/movie?title={}&year={}'.format(title,year))

def search_actors(name):
    return requestActor('GET', '/api/find/person?name={}'.format(name))    


@app.route('/go')
def go():
  return search_movies('transformers',2007)
  
def get_movie(movie_id):
  
    movie = request('GET', '/3/movie/{}?'.format(movie_id))
    movie = json.loads(movie)

    #add new movie to database
    try:
      print('The movie is added to the database')
    except BaseException as e:
      print('Could not insert data into the database. Response from API: ' + str(movie) + '    ' + str(e))

    print('Movie is in the database')
    return "movie in database"

if __name__ == '__main__':
    app.run()


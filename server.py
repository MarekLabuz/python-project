from flask import Flask, send_file, request, Response, jsonify, json
from flask_cors import CORS

# from api import search_movies_by_query
from util import get_movie, get_actor, search_movies_by_query, search_movies_by_person
import decimal


class MyJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
CORS(app)


@app.route('/')
def root():
    return send_file('./front/build/index.html', mimetype='text/html')


@app.route('/bundle.js')
def bundle():
    return send_file('./front/build/bundle.js', mimetype='text/javascript')


@app.route('/movies')
def movies():
    query = request.args.get('query')
    return Response(search_movies_by_query(query), mimetype='text/json')

@app.route('/movies-genre')
def movies():
    genre_id = request.args.get('genre_id')
    return Response(search_movies_by_genre(genre_id), mimetype='text/json')

@app.route('/movies-year')
def movies():
    year = request.args.get('year')
    return Response(search_movies_by_year(year), mimetype='text/json')


@app.route('/movie')
def movie():
    movie_id = request.args.get('id')
    actor_id = request.args.get('actor_id')
    return jsonify(get_movie(movie_id, actor_id))


@app.route('/actor')
def actor():
    actor_id = request.args.get('id')
    return jsonify(get_actor(actor_id))


@app.route('/movies-actor')
def movies_actor():
    actor_id = request.args.get('id')
    return Response(search_movies_by_person(actor_id), mimetype='text/json')


if __name__ == '__main__':
    app.run()


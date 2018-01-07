from flask import Flask, send_file, request, Response, jsonify
from flask_cors import CORS

# from api import search_movies_by_query
from util import get_movie, get_actor, search_movies_by_query, search_movies_by_person

app = Flask(__name__)
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


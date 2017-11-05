from flask import Flask, send_file, request, Response
from flask_cors import CORS

from api import search_movies_by_query

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

if __name__ == '__main__':
    app.run()
    # print(search_movies_by_query('lalaland'))



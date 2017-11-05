import http.client

BASE_URL = 'api.themoviedb.org'
API_KEY = 'ef3a8359454d45c5a58ad9e6dc9913e7'


def request(method, pathname):
    conn = http.client.HTTPSConnection(BASE_URL)
    payload = "{}"
    headers = {'content-type': 'application/json;charset=utf-8'}
    conn.request(method, '{}&api_key={}'.format(pathname, API_KEY), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')


def search_movies_by_query(query):
    return request('GET', '/3/search/movie?query={}'.format(query))

import html

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_caching import Cache

from movielist import MovieList

app = Flask(__name__)
CORS(app)
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1000
}
app.config.from_mapping(config)
cache = Cache(app)


@cross_origin()
@app.route('/allfilms/<username>')
@cache.memoize(1000)
def get_all_movies(username):
    username = html.escape(username)

    movies = MovieList(username)
    return movies.films


if __name__ == '__main__':
    app.run(debug=True)


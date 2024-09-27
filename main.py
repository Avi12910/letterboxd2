import html
import os

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_caching import Cache

from movielist import MovieList

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.environ.get("ALLOWED_ORIGINS", "*")}})
config = {
    "DEBUG":  os.environ.get("FLASK_DEBUG", False),
    "CACHE_TYPE": "SimpleCache",
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


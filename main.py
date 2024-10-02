import html
import os

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_caching import Cache

from backend.reccomender import recommend
from movielist import MovieList

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.environ.get("ALLOWED_ORIGINS", "*")}})
config = {
    "DEBUG": os.environ.get("FLASK_DEBUG", False),
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 600
}
app.config.from_mapping(config)
cache = Cache(app)


@cache.memoize(1000)
def get_movie_list(username):
    username = html.escape(username)
    movies = MovieList(username)
    return movies


@cross_origin()
@app.route('/allfilms/<username>')
def get_all_movies(username):
    movies = get_movie_list(username)
    return movies.films


@cross_origin()
@app.route('/')
def home():
    return 'Hello'


@cross_origin()
@app.route('/recommend/<username>')
def rec(username):
    movies = get_movie_list(username)
    recommendations = recommend(movies)
    return jsonify(recommendations)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

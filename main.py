

from flask import Flask
from flask_cors import CORS, cross_origin

from movielist import MovieList

app = Flask(__name__)
CORS(app)

@app.route('/allfilms/<username>')
@cross_origin
def get_all_movies(username):
    movies = MovieList(username)
    return movies.films

if __name__ == '__main__':
    app.run(debug=True)



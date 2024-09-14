import time
import requests
from bs4 import BeautifulSoup

from connect import exec_select, exec_insert
from movieinserts import insert_film
from utils import get_rating, collapse_data


class MovieList:

    def __init__(self, username):
        self.user = username

        # Access the users letterboxd all films page
        letterboxd = requests.get('https://letterboxd.com/' + self.user + '/films')
        soup = BeautifulSoup(letterboxd.text, 'html.parser')
        num_pages = int(soup.find_all(class_='paginate-page')[-1].get_text())
        film_ratings = {}

        # Get user info for each film on each page
        for i in range(0, num_pages + 1):
            letterboxd = requests.get('https://letterboxd.com/' + self.user  + '/films/page/' + str(i))
            soup = BeautifulSoup(letterboxd.text, 'html.parser')

            for poster in soup.find_all(class_='poster-container'):
                attr = poster.contents[1]
                film_ratings[attr.attrs['data-film-slug']] = get_rating(poster.get_text())

        # Get all IDs from the database

        film_ids = get_film_ids([*film_ratings])
        link_to_id = {name: ID for name, ID in film_ids}
        links_with_ids = {link for link, _ in film_ids}
        unmatched_links = [link for link in film_ratings if link not in links_with_ids]

        # If an ID is missing - add it to the database
        for link in unmatched_links:
            print('we got em chief ' + link)
            link_to_id[link] = insert_film(link)
            time.sleep(0.5)

        link_to_id = {name: ID for name, ID in film_ids}
        films = {link_to_id[name]: {'name': name, 'rating': rating} for name, rating in film_ratings.items() if
                   name in link_to_id}



        # Get film info for all IDs
        all_info = get_film_info([*films])
        for film_id, value in all_info.items():
            films[film_id]['film_info'] = value

        self._films = films

    @property
    def films(self):
        return self._films


def get_film_ids(links):
    return exec_select('dbo.tbl_films', ['link','id'], 'link', links)

def get_film_info(ids):

    all_films = {x: {} for x in ids}
    # for x in film_info:
    #     all_films[x[0]] = list(x[1::])

    all_info = exec_select('dbo.tbl_films','*', 'id',ids)
    for x in collapse_data(all_info):
        all_films[x[0]]['full_name'] = x[1][0][0]
        all_films[x[0]]['year'] = x[1][0][1]
        all_films[x[0]]['avg_rating'] = x[1][0][2]
        all_films[x[0]]['num_ratings'] = x[1][0][3]
        all_films[x[0]]['num_fans'] = x[1][0][4]
        all_films[x[0]]['length'] = x[1][0][5]
        all_films[x[0]]['genre'] = x[1][0][6]

    all_themes = get_themes(ids)
    for x in collapse_data(all_themes):
        all_films[x[0]]['themes'] = x[1]

    all_genres = get_genres(ids)
    for x in collapse_data(all_genres):
        all_films[x[0]]['genres'] = x[1]

    all_cast = get_cast(ids)
    for x in collapse_data(all_cast):
        all_films[x[0]]['cast'] = x[1]

    all_production = get_production(ids)
    for x in collapse_data(all_production):
        all_films[x[0]]['production'] = x[1]

    return all_films

def get_cast(film_ids):
    return exec_select('dbo.tbl_actorsinfilms',['film_id', 'actor_name'], 'film_id',film_ids)

def get_themes(film_ids):
    return exec_select('dbo.tbl_themesinfilms',['film_id', 'theme'], 'film_id',film_ids)

def get_genres(film_ids):
    return exec_select('dbo.tbl_genresinfilms',['film_id', 'genre'], 'film_id',film_ids)

def get_production(film_ids):
    return exec_select('dbo.tbl_productioninfilms',['film_id', 'production_name', 'production_type'], 'film_id',film_ids)

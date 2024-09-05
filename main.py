import time
from collections import defaultdict

from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS, cross_origin
import requests
from sys import getsizeof


from connect import exec_insert, exec_select, insert_film_basic

app = Flask(__name__)
CORS(app)

def get_user_profile(username):
    response = requests.get('https://letterboxd.com/' + username)
    return response.text

def get_film_info(links):

    film_info = exec_select('dbo.tbl_films','*', 'link',links)

    all_films = {}
    for x in film_info:
        all_films[x[0]] = list(x[1::])

    film_ids = list(all_films.keys())
    print(film_ids)

    all_themes = get_themes(film_ids)
    for x in collapse_data(all_themes):
        all_films[x[0]].append(x[1])

    all_genres = get_genres(film_ids)
    for x in collapse_data(all_genres):
        all_films[x[0]].append(x[1])

    all_cast = get_cast(film_ids)
    for x in collapse_data((all_cast)):
        all_films[x[0]].append(x[1])

    # film_info['production'] = get_production(film_ids)

    return all_films

def collapse_data(data):
    collapsed_data = defaultdict(list)
    for key, value in data:
        collapsed_data[key].append(value)
    result = [(key, value) for key, value in collapsed_data.items()]
    return result

def insert_film(link):
    film = scrape_film_basic(link)

    film_id = insert_film_basic([film['link'],film['name'],film['release_year'],film['avg_rating'],film['num_ratings'],film['num_fans'],film['length'],film['language']])

    insert_cast(film_id, film['cast'])
    insert_genres(film_id, film['genres'])
    insert_themes(film_id, film['themes'])
    insert_production(film_id, film['production'])

    return film

def get_cast(film_ids):
    return exec_select('dbo.tbl_actorsinfilms',['film_id', 'actor_name'], 'film_id',film_ids)

def get_themes(film_ids):
    return exec_select('dbo.tbl_themesinfilms',['film_id', 'theme'], 'film_id',film_ids)

def get_genres(film_ids):
    return exec_select('dbo.tbl_genresinfilms',['film_id', 'genre'], 'film_id',film_ids)

def get_production(film_ids):
    return exec_select('dbo.tbl_productioninfilms',['film_id', 'production_name', 'production_type'], 'film_id',film_ids)

def insert_cast(film_id, cast):
    if cast:
        values = [(film_id, x) for x in cast]
        exec_insert('dbo.tbl_actorsinfilms', ('film_id', 'actor_name'), values)

def insert_genres(film_id, genres):
    values = [(film_id, x) for x in genres]
    exec_insert('dbo.tbl_genresinfilms',('film_id','genre'), values)

def insert_themes(film_id, themes):
    if themes:
        values = [(film_id, x) for x in themes]
        exec_insert('dbo.tbl_themesinfilms', ('film_id', 'theme'), values)

def insert_production(film_id, production):
    values = [(film_id, x, y) for x, y in production]
    exec_insert('dbo.tbl_productioninfilms',('film_id','production_type','production_name'), values)

def get_film(link):
    film_info = exec_select('dbo.tbl_films','*', 'link',link)
    if film_info is None:
        return insert_film(link)

    else:
        return film_info

# Gets name, release date, cast, length, avg_rating, num_ratings
def scrape_film_basic(link):
    basic_info = {'link': link}

    film_basic = requests.get('https://letterboxd.com/film/' + link)
    soup = BeautifulSoup(film_basic.text, 'html.parser')

    avg_rating = soup.find('meta', content='Average rating').find_next()['content']
    avg_rating = avg_rating.split(' ')[0]
    basic_info['avg_rating'] = avg_rating

    release_year = soup.find(class_='releaseyear').get_text()
    basic_info['release_year'] = release_year

    film_name = soup.find(class_='name js-widont prettify').get_text() + ' (' + release_year + ')'
    basic_info['name'] = film_name

    film_length = soup.find(class_='text-link text-footer').get_text(strip=True).replace('\xa0',' ').split(' ')[0]
    basic_info['length'] = film_length

    soup_cast = soup.find(class_='cast-list text-sluglist')
    if soup_cast:
        film_cast = [x.get_text() for x in soup.find(class_='cast-list text-sluglist').find_all('a') if
                     x.get_text() != 'Show All…']
        basic_info['cast'] = film_cast
    else:
        basic_info['cast'] = []

    film_production = []
    film_production.extend(scrape_film_production(soup, 'Director'))
    film_production.extend(scrape_film_production(soup, 'Writer'))
    film_production.extend(scrape_film_production(soup, 'Composer'))

    basic_info['production'] = film_production

    film_language = soup.find(string=['Language', 'Languages', 'Primary Language']).find_parent().find_parent().find_next_sibling().find('a').get_text()
    basic_info['language'] = film_language

    soup_genres = soup.find(id='tab-genres').find_all('div')
    film_genres = [g.get_text() for g in soup_genres[0].find_all('a')]
    basic_info['genres'] = film_genres

    if len(soup_genres) > 1:
        film_themes = [g.get_text() for g in soup_genres[1].find_all('a')][:-1]
        basic_info['themes'] = film_themes
    else:
        basic_info['themes'] = []

    ratings_hist = requests.get('https://letterboxd.com/csi/film/' + link + '/rating-histogram/')
    ratings_soup = BeautifulSoup(ratings_hist.text, 'html.parser')

    ratings_nums = [x.get_text().split(' ') for x in ratings_soup.find('ul').children if x != ' ']
    num_ratings = sum([int(x[1].replace(u'\xa0', u' ').split(' ')[0].replace(',', '')) for x in
                       ratings_nums if len(x) > 1])

    basic_info['num_ratings'] = num_ratings

    soup_fans = ratings_soup.find(class_='all-link more-link')
    if soup_fans:
        num_fans = soup_fans.get_text().split(' ')[0]
        if 'K' in num_fans:
            num_fans = float(num_fans.replace('K', ''))
            num_fans = int(num_fans * 1000)
        basic_info['num_fans'] = num_fans
    else:
        basic_info['num_fans'] = 0

    return basic_info

def scrape_film_production(soup, role):
    value = []

    soup2 = soup.find(string=[role, role + 's'])
    if soup2 is not None:
        film_production = [d.get_text() for d in
                           soup2.find_parent().find_parent().find_next_sibling().find_all('a')]
        for d in film_production:
            value.append((role, d))

    return value

def film_in_db(link):
    return exec_select('dbo.tbl_films',['id'],'link',[link])

# @app.route('/allfilms/<username>')
# @cross_origin()
def get_all_watched_movies(username):
    films = requests.get('https://letterboxd.com/' + username + '/films')
    soup = BeautifulSoup(films.text, 'html.parser')
    num_pages = int(soup.find_all(class_='paginate-page')[-1].get_text())
    print(num_pages)
    all_films = []

    for i in range(num_pages + 1):
        films = requests.get('https://letterboxd.com/' + username + '/films/page/' + str(i))
        soup = BeautifulSoup(films.text, 'html.parser')

        for poster in soup.find_all(class_='poster-container'):
            attr = poster.contents[1]
            film = {'link': attr.attrs['data-film-slug']}
            print(film['link'])
            film_id = film_in_db(film['link'])['id']
            film_info = None
            if not film_id:
                film_info = insert_film(film['link'])
                time.sleep(0.5)
            else:
                film_info = get_film_info(film_id)
            all_films.append(film_info)

    return all_films


if __name__ == '__main__':
    # li = exec_select('dbo.tbl_films','*', 'id',[18,19])

    print(get_film_info(['longlegs','barbie']))
    # print(get_all_watched_movies('Avi1291'))


import time

from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS, cross_origin
import requests
import psycopg2

from config import load_config

ratings = {'': 'n/a',
           '½': 0.5,
           '★': 1,
           '★½': 1.5,
           '★★': 2,
           '★★½': 2.5,
           '★★★': 3,
           '★★★½': 3.5,
           '★★★★': 4,
           '★★★★½': 4.5,
           '★★★★★': 5}

app = Flask(__name__)
CORS(app)


def insert_actor(actor_name):
    sql = """INSERT INTO dbo.tbl_actors(actor_name)
             VALUES(%s) RETURNING \"actor_ID\";"""

    actor_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (actor_name,))

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    actor_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return actor_id


def get_rating(stars):
    if stars is None:
        return 'n/a'
    else:
        return ratings[stars.strip()]


def get_user_profile(username):
    response = requests.get('https://letterboxd.com/' + username)
    return response.text


def get_film_info(link):
    film_info = {}

    # film_info['genres'] = get_film_genres(link)

    return film_info


def insert_film(link):
    film = get_film_basic(link)

    film_id = insert_film_basic([film['link'],film['name'],film['release_year'],film['avg_rating'],film['num_ratings'],film['num_fans'],film['length'],film['language']])

    insert_cast(film_id, film['cast'])
    insert_genres(film_id, film['genres'])
    insert_themes(film_id, film['themes'])
    insert_production(film_id, film['production'])


def insert_film_basic(film):
    sql = """INSERT INTO dbo.tbl_films(link,name,release_year,avg_rating,num_ratings,num_fans,length,language) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""

    film_id = None

    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, film)

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    film_id = rows[0]

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return film_id

def get_cast(film_id):
    sql = """SELECT * FROM dbo.tbl_actorsinfilms WHERE film_id = %s"""
    return exec_select(sql, film_id)

def get_themes(film_id):
    sql = """SELECT * FROM dbo.tbl_themesinfilms WHERE film_id = %s"""
    return exec_select(sql, film_id)

def get_genres(film_id):
    sql = """SELECT * FROM dbo.tbl_genresinfilms WHERE film_id = %s"""
    return exec_select(sql, film_id)

def get_production(film_id):
    sql = """SELECT * FROM dbo.tbl_productioninfilms WHERE film_id = %s"""
    return exec_select(sql, film_id)

def insert_cast(film_id, cast):
    if cast:
        values = [(film_id, x) for x in cast]
        sql = """INSERT INTO dbo.tbl_actorsinfilms(film_id, actor_name)
                     VALUES """

        exec_insert(sql, values)

def insert_genres(film_id, genres):
    values = [(film_id, x) for x in genres]
    sql = """INSERT INTO dbo.tbl_genresinfilms(film_id, genre)
                     VALUES """

    exec_insert(sql, values)

def insert_themes(film_id, themes):
    if themes:
        values = [(film_id, x) for x in themes]
        sql = """INSERT INTO dbo.tbl_themesinfilms(film_id, theme)
                         VALUES """

        exec_insert(sql, values)

def insert_production(film_id, production):
    values = [(film_id, x, y) for x, y in production]
    sql = """INSERT INTO dbo.tbl_productioninfilms(film_id, production_type, production_name)
                         VALUES """

    exec_insert(sql, values)

def generate_args_string(values):
    args_str = ",".join("(%s)" % ", ".join("%s" for _ in range(len(t))) for t in values)
    return args_str


def exec_insert(sql, values):
    config = load_config()
    args_str = generate_args_string(values)
    sql = sql + args_str
    flattened_values = [item for sublist in values for item in sublist]
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, flattened_values)
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def exec_select(sql, key):
    config = load_config()
    result = None
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (key,))
                result = cur.fetchall()
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return result

def get_film(name):
    sql = """SELECT * FROM dbo.tbl_films WHERE name = %s"""

    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (name, ))

                film_info = cur.fetch()

                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    if film_info is None:
        return insert_film(name)

    else:
        return film_info

# Gets name, release date, cast, length, avg_rating, num_ratings
def get_film_basic(link):
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
    film_production.extend(get_film_production(soup, 'Director'))
    film_production.extend(get_film_production(soup, 'Writer'))
    film_production.extend(get_film_production(soup, 'Composer'))

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

def get_film_production(soup, role):
    value = []

    soup2 = soup.find(string=[role, role + 's'])
    if soup2 is not None:
        film_production = [d.get_text() for d in
                           soup2.find_parent().find_parent().find_next_sibling().find_all('a')]
        for d in film_production:
            value.append((role, d))

    return value

def film_in_db(link):
    sql = """SELECT * FROM dbo.tbl_films WHERE link = %s"""
    return exec_select(sql, link) != []



# @app.route('/allfilms/<username>')
# @cross_origin()
def get_all_watched_movies(username):
    films = requests.get('https://letterboxd.com/imthelizardking/list/all-the-movies-10k-views-4/by/popular/')
    soup = BeautifulSoup(films.text, 'html.parser')
    num_pages = int(soup.find_all(class_='paginate-page')[-1].get_text())
    print(num_pages)
    film_names = []

    for i in range(95, num_pages + 1):
        films = requests.get('https://letterboxd.com/imthelizardking/list/all-the-movies-10k-views-4/by/popular/page/' + str(i))
        soup = BeautifulSoup(films.text, 'html.parser')

        for poster in soup.find_all(class_='poster-container'):
            attr = poster.contents[1]
            film = {'name': attr.attrs['data-film-slug']}
            print(film['name'], i)
            if not film_in_db(film['name']):
                insert_film(film['name'])
                time.sleep(0.5)



if __name__ == '__main__':
    get_all_watched_movies('punq')
import psycopg2
import os

from psycopg2 import sql

env = {
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME'],
    'user': os.environ['DB_USERNAME'],
    'password': os.environ['DB_PASSWORD']
}

def insert_film_basic(film):
    sql = """INSERT INTO dbo.tbl_films(link,name,release_year,avg_rating,num_ratings,num_fans,length,language) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
    film_id = None

    try:
        with  psycopg2.connect(**env) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, film)

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    film_id = rows[0]

                print(cur.query)
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return film_id


def exec_insert(table, columns, values):
    insert_query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({placeholders})").format(
        table=sql.Identifier('dbo',table),
        columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
        placeholders=sql.SQL(', ').join(sql.Placeholder() for _ in columns)
    )

    try:
        with  psycopg2.connect(**env) as conn:
            with  conn.cursor() as cur:
                print(insert_query.as_string(conn))
                cur.executemany(insert_query, values)
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def exec_select(table, columns, key, values):

    if len(values) <= 1:
        select_query = sql.SQL("SELECT {columns} FROM {table} WHERE {key} = {values}").format(
            table=sql.SQL(table),
            columns=sql.SQL('*') if columns == '*' else sql.SQL(', ').join(map(sql.Identifier, columns)),
            key=sql.Identifier(key),
            values=sql.Placeholder()
        )
    else:
        select_query = sql.SQL("SELECT {columns} FROM {table} WHERE {key} IN ({values})").format(
            table=sql.SQL(table),
            columns=sql.SQL('*') if columns == '*' else sql.SQL(', ').join(map(sql.Identifier, columns)),
            key=sql.Identifier(key),
            values=sql.SQL(', ').join(sql.Placeholder() for _ in values)
        )

    result = None

    try:
        with  psycopg2.connect(**env) as conn:
            with  conn.cursor() as cur:
                cur.execute(select_query, values)
                rows = cur.fetchall()
                result = rows
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return result
from contextlib import contextmanager
import sqlite3

DB = 'test.db'


@contextmanager
def SQLite(db):
    conn = sqlite3.connect(db)

    try:
        yield conn.cursor()

    finally:
        conn.commit()
        conn.close()


def init_db(db):
    with SQLite(db) as cur:
        cur.execute(
            'CREATE TABLE recipe('
            'id integer primary key,'
            'name text unique not null,'
            'servings numeric,'
            'method text,'
            'tags text'
            ')'
        )

        cur.execute(
            'CREATE TABLE ingredient('
            'id integer primary key,'
            'name text unique not null'
            ')'
        )

        cur.execute(
            'CREATE TABLE recipe_ingredient('
            'recipe_id integer,'
            'ingredient_id integer,'
            'quantity numeric,'
            'measure text,'
            'FOREIGN KEY(recipe_id) REFERENCES recipe(id),'
            'FOREIGN KEY(ingredient_id) REFERENCES ingredient(id)'
            ')'
        )

        cur.execute(
            'CREATE TABLE mealplan('
            'id integer primary key,'
            'date date,'
            'name text,'
            'servings numeric'
            ')'
        )


def cur_to_dicts(cur):
    cols = [c[0] for c in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]

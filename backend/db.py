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


def get_recipe_ingredients():
    with SQLite(DB) as cur:
        cur.execute(
            'SELECT '
            'ingredient.name name,'
            'recipe_ingredient.* '
            'FROM ingredient '
            'JOIN recipe_ingredient ON recipe_ingredient.ingredient_id = ingredient.id '
        )
        return cur_to_dicts(cur)


def get_mealplans():
    with SQLite(DB) as cur:
        cur.execute('select * from mealplan')
        return cur_to_dicts(cur)


def create_mealplan(date, name, servings):
    with SQLite(DB) as cur:
        cur.execute('INSERT INTO mealplan(date, name, servings) VALUES (?,?,?)', (date, name, servings))

        cur.execute('SELECT * FROM mealplan WHERE date = ? AND name = ?', (date, name))

        return cur_to_dicts(cur)[0]

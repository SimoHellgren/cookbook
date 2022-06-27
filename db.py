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


def get_recipes():
    with SQLite(DB) as cur:
        cur.execute('select * from recipe')
        return cur_to_dicts(cur)


def get_recipe_by_id(id):
    with SQLite(DB) as cur:
        cur.execute('select * from recipe where id = ?', (id,))
        return cur_to_dicts(cur)[0]


def get_recipe_ingredients_by_recipe_id(id):
    with SQLite(DB) as cur:
        cur.execute(
            'SELECT '
            'ingredient.name name,'
            'recipe_ingredient.* '
            'FROM ingredient '
            'JOIN recipe_ingredient ON recipe_ingredient.ingredient_id = ingredient.id '
            'WHERE recipe_ingredient.recipe_id = ?',
            (id,)
        )
        return cur_to_dicts(cur)


def create_recipe(name, servings, method, tags=None):
    with SQLite(DB) as cur:
        cur.execute('INSERT OR IGNORE INTO recipe(name, servings, method, tags) values (?,?,?,?)', (name, servings, method, tags))

        # SQLite doesn't support RETURNING, so we query for the new record separately
        cur.execute('SELECT * FROM recipe where name == ?', (name,))
        return cur_to_dicts(cur)[0]


def create_ingredient(name):
    with SQLite(DB) as cur:
        cur.execute('INSERT OR IGNORE INTO ingredient(name) values (?)', (name,))

        # SQLite doesn't support RETURNING, so we query for the new record separately
        cur.execute('SELECT * FROM ingredient where name == ?', (name,))
        return cur_to_dicts(cur)[0]


def create_recipe_ingredient(recipe_id, ingredient_id, quantity, measure):
    with SQLite(DB) as cur:
        cur.execute('INSERT OR IGNORE INTO recipe_ingredient(recipe_id, ingredient_id, quantity, measure) values (?,?,?,?)', (recipe_id, ingredient_id, quantity, measure))

        # SQLite doesn't support RETURNING, so we query for the new record separately
        cur.execute('SELECT * FROM recipe_ingredient where recipe_id = ? AND ingredient_id = ?', (recipe_id, ingredient_id))
        return cur_to_dicts(cur)[0]


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

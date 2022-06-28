from backend.db import SQLite, cur_to_dicts, DB


def get_all():
    with SQLite(DB) as cur:
        cur.execute('select * from recipe')
        return cur_to_dicts(cur)


def get(id):
    with SQLite(DB) as cur:
        cur.execute('select * from recipe where id = ?', (id,))
        return cur_to_dicts(cur)[0]


def create(name, servings, method, tags=None):
    with SQLite(DB) as cur:
        cur.execute('INSERT OR IGNORE INTO recipe(name, servings, method, tags) values (?,?,?,?)', (name, servings, method, tags))

        # SQLite doesn't support RETURNING, so we query for the new record separately
        cur.execute('SELECT * FROM recipe where name == ?', (name,))
        return cur_to_dicts(cur)[0]


def get_ingredients(id):
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


def add_ingredient(recipe_id, ingredient_id, quantity, measure):
    with SQLite(DB) as cur:
        cur.execute('INSERT OR IGNORE INTO recipe_ingredient(recipe_id, ingredient_id, quantity, measure) values (?,?,?,?)', (recipe_id, ingredient_id, quantity, measure))

        # SQLite doesn't support RETURNING, so we query for the new record separately
        cur.execute('SELECT * FROM recipe_ingredient where recipe_id = ? AND ingredient_id = ?', (recipe_id, ingredient_id))
        return cur_to_dicts(cur)[0]

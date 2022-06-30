from backend.db import SQLite, cur_to_dicts, DB


def get_all():
    with SQLite(DB) as cur:
        cur.execute('select * from mealplan')
        return cur_to_dicts(cur)


def get(id):
    with SQLite(DB) as cur:
        cur.execute('SELECT * FROM mealplan WHERE id = ?', (id,))
        return cur_to_dicts(cur)[0]


def create(date, name, servings):
    with SQLite(DB) as cur:
        cur.execute('INSERT INTO mealplan(date, name, servings) VALUES (?,?,?)', (date, name, servings))

        cur.execute('SELECT * FROM mealplan WHERE date = ? AND name = ?', (date, name))

        return cur_to_dicts(cur)[0]


def update(id, date, name, servings, recipe_id):
    with SQLite(DB) as cur:
        cur.execute(
            'UPDATE mealplan SET '
            'date = ? '
            'name = ? '
            'servings = ? '
            'recipe_id = ? '
            'WHERE id = ?',
            (date, name, servings, recipe_id, id)
        )

        cur.execute('SELECT * FROM mealplan WHERE id = ?', (id,))
        return cur_to_dicts(cur)[0]


def delete(id):
    with SQLite(DB) as cur:
        cur.execute('DELETE FROM mealplan WHERE id = ?', (id,))

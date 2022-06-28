from backend.db import SQLite, cur_to_dicts, DB


def get_all():
    with SQLite(DB) as cur:
        cur.execute('select * from mealplan')
        return cur_to_dicts(cur)


def create(date, name, servings):
    with SQLite(DB) as cur:
        cur.execute('INSERT INTO mealplan(date, name, servings) VALUES (?,?,?)', (date, name, servings))

        cur.execute('SELECT * FROM mealplan WHERE date = ? AND name = ?', (date, name))

        return cur_to_dicts(cur)[0]

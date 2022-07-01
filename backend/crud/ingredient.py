from backend.db import SQLite, cur_to_dicts, DB


def get_all():
    with SQLite(DB) as cur:
        cur.execute("SELECT * FROM ingredient")
        return cur_to_dicts(cur)


def create(name):
    with SQLite(DB) as cur:
        cur.execute("INSERT OR IGNORE INTO ingredient(name) values (?)", (name,))

        # SQLite doesn't support RETURNING, so we query for the new record separately
        cur.execute("SELECT * FROM ingredient where name == ?", (name,))
        return cur_to_dicts(cur)[0]

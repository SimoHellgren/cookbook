from backend.db import SQLite, cur_to_dicts, DB


def get_all():
    with SQLite(DB) as cur:
        cur.execute(
            "SELECT "
            "ingredient.name name,"
            "recipe_ingredient.* "
            "FROM ingredient "
            "JOIN recipe_ingredient ON recipe_ingredient.ingredient_id = ingredient.id "
        )
        return cur_to_dicts(cur)

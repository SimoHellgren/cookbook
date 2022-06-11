import os
import json

BASEPATH = "./recipes"


def read_recipes():
    for filename in os.listdir(BASEPATH):
        if not filename.endswith("json"):
            continue

        with open(os.path.join(BASEPATH, filename), "r", encoding="utf-8") as f:
            yield json.load(f)


def create_recipe(filename, name, portions, ingredients, method, tags=None):
    if not tags:
        tags = []
    with open(os.path.join(BASEPATH, filename), "w") as f:
        json.dump(
            {"name": name, "portions": portions, "ingredients": ingredients, "method": method, "tags": tags},
            f,
        )


def read_mealplan():
    with open("./mealplan/mealplan.json", "r") as f:
        return json.load(f)


def write_mealplan(mp):
    with open('./mealplan/mealplan.json', 'w') as f:
        json.dump(mp, f)

import os
import json


def read_recipes():
    basepath = "./recipes"
    for filename in os.listdir(basepath):
        if not filename.endswith("json"):
            continue

        with open(os.path.join(basepath, filename), "r", encoding="utf-8") as f:
            yield json.load(f)


def create_recipe(filename, name, ingredients, method):
    with open(f"./recipes/{filename}", "w") as f:
        json.dump({"name": name, "ingredients": ingredients, "method": method}, f)

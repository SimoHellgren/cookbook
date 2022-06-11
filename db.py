import os
import json


def read_recipes():
    basepath = "./recipes"
    for filename in os.listdir(basepath):
        if not filename.endswith("json"):
            continue

        with open(os.path.join(basepath, filename), "r", encoding="utf-8") as f:
            yield json.load(f)

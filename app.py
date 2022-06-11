from itertools import chain

from flask import Flask, render_template, request

from db import create_recipe, read_recipes

app = Flask(__name__)


@app.route("/")
def recipes():
    recipes = list(read_recipes())

    filters = request.args.get("tags")

    filtered_by_tags = (
        filter(lambda r: all(tag in r["tags"] for tag in filters.split(",")), recipes)
        if filters
        else recipes
    )

    search = request.args.get("search", "").lower()
    filter_by_search = (r for r in filtered_by_tags if search in r["name"].lower())

    recipes_to_show = list(filter_by_search)

    available_tags = sorted(
        set(chain.from_iterable(r["tags"] for r in recipes_to_show))
    )

    return render_template(
        "recipes.html", recipes=list(recipes_to_show), tags=available_tags
    )


@app.route("/add_recipe", methods=("GET", "POST"))
def add_recipe():
    if request.method == "POST":
        name = request.form["name"]

        ingredient_list = (
            i.split(";") for i in request.form["ingredients"].split("\r\n")
        )
        cols = ("name", "quantity", "measure")
        ingredients = [dict(zip(cols, row)) for row in ingredient_list]

        method = request.form["method"]

        tags = [t.strip() for t in request.form["tags"].split(",")]

        create_recipe(
            f"{name.lower().replace(' ', '_')}.json",
            name=name,
            ingredients=ingredients,
            method=method,
            tags=tags,
        )

    return render_template("add_recipe.html")

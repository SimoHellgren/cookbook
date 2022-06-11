from flask import Flask, render_template, request

from db import create_recipe, read_recipes

app = Flask(__name__)


@app.route("/")
def recipes():
    recipes = list(read_recipes())
    return render_template("recipes.html", recipes=recipes)


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

from flask import Flask, render_template

from db import read_recipes

app = Flask(__name__)


@app.route("/")
def recipes():
    recipes = list(read_recipes())
    return render_template("recipes.html", recipes=recipes)


@app.route("/add_recipe")
def add_recipe():
    return render_template("add_recipe.html")

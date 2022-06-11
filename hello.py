from flask import Flask, render_template

from db import read_recipes

app = Flask(__name__)


@app.route("/")
def hello():
    recipes = list(read_recipes())
    return render_template("base.html", recipes=recipes)

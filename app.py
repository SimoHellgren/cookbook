from functools import partial
import os
from itertools import chain, groupby

import requests

from flask import Flask, render_template, request

from backend.api import api
from backend import crud

template_dir = os.path.abspath('./frontend/templates')
app = Flask(__name__, template_folder=template_dir)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(api.bp)

API_BASE_URL = 'http://localhost:5000/api'

apirequest = lambda method, endpoint, *args, **kwargs: requests.request(method, API_BASE_URL + endpoint, *args, **kwargs)  # noqa E731
get = partial(apirequest, 'GET')
post = partial(apirequest, 'POST')


@app.route("/")
@app.route("/recipes")
def recipes():
    # recipes = get('/recipes').json()
    # ingredients = get('/recipe_ingredients').json()
    recipes = crud.recipe.get_all()
    ingredients = crud.ingredient.get_all()

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
        set(chain.from_iterable(r["tags"].split(',') for r in recipes_to_show))
    )

    return render_template(
        "recipes.html", recipes=recipes_to_show, ingredients=ingredients, tags=available_tags
    )


@app.route("/recipes/<id>", methods=("GET", "POST"))
def get_recipe(id):
    # recipe = get(f'/recipes/{id}').json()
    # ingredients = get(f'/recipes/{id}/ingredients').json()
    recipe = crud.recipe.get(id)
    ingredients = crud.recipe.get_ingredients(id)

    return render_template(
        "recipe.html", recipe=recipe, ingredients=ingredients
    )


def recipe_from_form(form):
    name = form["name"]
    servings = form["servings"]
    method = form["method"]
    tags = form["tags"].strip()

    ingredient_keys = sorted(k for k in form if k.startswith('ingredient'))
    quantity_keys = sorted(k for k in form if k.startswith('quantity'))
    measure_keys = sorted(k for k in form if k.startswith('measure'))

    ingredients = [
        {'name': form[k1], 'quantity': form[k2], 'measure': form[k3]}
        for k1, k2, k3 in zip(ingredient_keys, quantity_keys, measure_keys)
    ]

    return {
        "name": name,
        "servings": servings,
        "method": method,
        "tags": tags,
    }, ingredients


@app.route("/add_recipe", methods=("GET", "POST"))
def add_recipe():
    if request.method == "POST":

        recipe, ingredients = recipe_from_form(request.form)

        db_recipe = post('/recipes', json=recipe).json()

        for ingredient in ingredients:
            db_ingredient = post('/ingredients', json=ingredient).json()
            recipe_ingredient_data = {
                'ingredient_id': db_ingredient['id'],
                'quantity': ingredient['quantity'],
                'measure': ingredient['measure']
            }

            post(f"/recipes/{db_recipe['id']}/ingeredients", json=recipe_ingredient_data)

    return render_template("add_recipe.html")


@app.route("/mealplan", methods=("GET", "POST"))
def mealplan():
    # mp = get('/mealplans').json()
    mp = crud.mealplan.get_all()
    if request.method == "POST":
        date = request.form["date"]

        form_meals = filter(None, request.form["meals"].split("\r\n"))
        cols = ("name", "servings")

        meals = [dict(zip(cols, row.split(";")), date=date) for row in form_meals]

        db_meals = [post('/mealplans', json=meal).json() for meal in meals]

        mp = [*db_meals, *mp]  # mutation :|

    return render_template(
        "mealplan.html", mealplan=sorted(mp, key=lambda x: x["date"], reverse=True)
    )


@app.route("/shoppinglist", methods=("GET", "POST"))
def shopping_list():
    # all_recipes = get('/recipes').json()
    all_recipes = crud.recipe.get_all()
    items = []
    if request.method == "POST":
        choices = request.form.getlist("recipes")
        ingredients = chain.from_iterable(
            get(f"/recipes/{r['id']}/ingredients").json() for r in all_recipes if r["name"] in choices
        )

        kf = lambda x: (x["name"], x["measure"])  # noqa: E731
        gb = groupby(sorted(ingredients, key=kf), key=kf)

        items = [
            {
                "name": name,
                "measure": measure,
                "quantity": sum(float(row["quantity"]) for row in rows),
            }
            for (name, measure), rows in gb
        ]

    return render_template("shoppinglist.html", recipes=all_recipes, items=items)

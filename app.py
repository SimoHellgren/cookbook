from itertools import chain, groupby

from flask import Flask, render_template, request

from db import create_ingredient, create_mealplan, create_recipe, create_recipe_ingredient, get_mealplans, get_recipe_by_id, get_recipe_ingredients, get_recipe_ingredients_by_recipe_id, get_recipes

from backend import api

app = Flask(__name__)

app.register_blueprint(api.bp)


@app.route("/")
@app.route("/recipes")
def recipes():
    recipes = get_recipes()
    ingredients = get_recipe_ingredients()

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


def recipe_from_form(form):
    name = form["name"]

    servings = form["portions"]

    ingredient_list = (i.split(";") for i in form["ingredients"].split("\r\n"))
    cols = ("name", "quantity", "measure")
    ingredients = [dict(zip(cols, row)) for row in ingredient_list]

    method = form["method"]

    tags = form["tags"].strip()

    return {
        "name": name,
        "servings": servings,
        "method": method,
        "tags": tags,
    }, ingredients


@app.route("/recipes/<id>", methods=("GET", "POST"))
def get_recipe(id):
    recipe = get_recipe_by_id(id)
    ingredients = get_recipe_ingredients_by_recipe_id(id)

    if request.method == "POST":
        recipe, ingredients = recipe_from_form(request.form)  # mutation :|
        db_recipe = create_recipe(**recipe)

        for ingredient in ingredients:
            db_ingredient = create_ingredient(ingredient['name'])
            create_recipe_ingredient(db_recipe['id'], db_ingredient['id'], ingredient['quantity'], ingredient['measure'])

    ingredientstring = "\r\n".join(
        f"{i['name']};{i['quantity']};{i['measure']}" for i in ingredients
    )
    return render_template(
        "recipe.html", recipe=recipe, ingredientstring=ingredientstring
    )


@app.route("/add_recipe", methods=("GET", "POST"))
def add_recipe():
    if request.method == "POST":

        recipe, ingredients = recipe_from_form(request.form)

        db_recipe = create_recipe(**recipe)

        for ingredient in ingredients:
            db_ingredient = create_ingredient(ingredient['name'])
            create_recipe_ingredient(db_recipe['id'], db_ingredient['id'], ingredient['quantity'], ingredient['measure'])

    return render_template("add_recipe.html")


@app.route("/mealplan", methods=("GET", "POST"))
def mealplan():
    mp = get_mealplans()
    if request.method == "POST":
        date = request.form["date"]

        form_meals = filter(None, request.form["meals"].split("\r\n"))
        cols = ("name", "servings")

        meals = [dict(zip(cols, row.split(";")), date=date) for row in form_meals]

        for meal in meals:
            create_mealplan(**meal)

        mp = [*meals, *mp]  # mutation :|

    return render_template(
        "mealplan.html", mealplan=sorted(mp, key=lambda x: x["date"], reverse=True)
    )


@app.route("/shoppinglist", methods=("GET", "POST"))
def shopping_list():
    all_recipes = get_recipes()
    items = []
    if request.method == "POST":
        choices = request.form.getlist("recipes")
        ingredients = chain.from_iterable(
            get_recipe_ingredients_by_recipe_id(r['id']) for r in all_recipes if r["name"] in choices
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

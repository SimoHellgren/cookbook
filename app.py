from itertools import chain, groupby

from flask import Flask, render_template, request

from db import create_recipe, read_recipes, read_mealplan, write_mealplan

app = Flask(__name__)


@app.route("/")
@app.route("/recipes")
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


def recipe_from_form(form):
    name = form["name"]

    portions = form["portions"]

    ingredient_list = (i.split(";") for i in form["ingredients"].split("\r\n"))
    cols = ("name", "quantity", "measure")
    ingredients = [dict(zip(cols, row)) for row in ingredient_list]

    method = form["method"]

    tags = [t.strip() for t in form["tags"].split(",")]

    return {
        "name": name,
        "portions": portions,
        "ingredients": ingredients,
        "method": method,
        "tags": tags,
    }


@app.route("/recipes/<id>", methods=("GET", "POST"))
def get_recipe(id):
    recipe = next(r for r in read_recipes() if r["name"] == id)

    if request.method == "POST":
        recipe = recipe_from_form(request.form)  # mutation :|
        create_recipe(f"{recipe['name'].lower().replace(' ', '_')}.json", **recipe)

    ingredientstring = "\r\n".join(
        f"{i['name']};{i['quantity']};{i['measure']}" for i in recipe["ingredients"]
    )
    return render_template(
        "recipe.html", recipe=recipe, ingredientstring=ingredientstring
    )


@app.route("/add_recipe", methods=("GET", "POST"))
def add_recipe():
    if request.method == "POST":

        recipe = recipe_from_form(request.form)

        create_recipe(f"{recipe['name'].lower().replace(' ', '_')}.json", **recipe)

    return render_template("add_recipe.html")


@app.route("/mealplan", methods=("GET", "POST"))
def mealplan():
    mp = read_mealplan()
    if request.method == "POST":
        date = request.form["date"]

        form_meals = filter(None, request.form["meals"].split("\r\n"))
        cols = ("name", "portions")

        meals = [dict(zip(cols, row.split(";"))) for row in form_meals]

        mp = [{"date": date, "meals": meals}, *mp]  # mutation :|
        write_mealplan(mp)

    return render_template(
        "mealplan.html", mealplan=sorted(mp, key=lambda x: x["date"], reverse=True)
    )


@app.route("/shoppinglist", methods=("GET", "POST"))
def shopping_list():
    all_recipes = list(read_recipes())
    items = []
    if request.method == "POST":
        choices = request.form.getlist("recipes")
        ingredients = chain.from_iterable(
            r["ingredients"] for r in all_recipes if r["name"] in choices
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

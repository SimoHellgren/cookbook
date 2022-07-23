from functools import partial
import os
from itertools import chain, groupby, count
from datetime import datetime, timedelta
from typing import Iterator, Tuple
from flask import abort
from werkzeug.datastructures import ImmutableMultiDict

import requests

from flask import Flask, render_template, request


template_dir = os.path.abspath("./frontend/templates")
app = Flask(__name__, template_folder=template_dir)
app.config["TEMPLATES_AUTO_RELOAD"] = True


API_BASE_URL = "http://localhost:8000"

apirequest = lambda method, endpoint, *args, **kwargs: requests.request(  # noqa: E731
    method, API_BASE_URL + endpoint, *args, **kwargs
)
get = partial(apirequest, "GET")
post = partial(apirequest, "POST")


def datetime_range(
    start: datetime, end: datetime, step: timedelta = timedelta(days=1)
) -> Iterator[datetime]:
    """like range, but for datetimes and you must always specify both start and end."""
    deltas = (step * i for i in count(0))

    for delta in deltas:
        if start + delta >= end:
            return

        yield start + delta


@app.route("/")
@app.route("/recipes")
def recipes() -> str:
    recipes = get("/recipes").json()

    if not recipes:
        abort(404)

    filters = request.args.get("tags")

    filtered_by_tags = (
        filter(lambda r: all(tag in r.tags for tag in filters.split(",")), recipes)  # type: ignore[arg-type,operator]
        if filters
        else recipes
    )

    search = request.args.get("search", "").lower()
    filter_by_search = (r for r in filtered_by_tags if search in r["name"].lower())  # type: ignore[attr-defined]

    recipes_to_show = list(filter_by_search)

    available_tags = sorted(
        set(chain.from_iterable(r["tags"].split(",") for r in recipes_to_show))  # type: ignore[attr-defined]
    )

    return render_template(
        "recipes.html",
        recipes=recipes_to_show,
        tags=available_tags,
    )


@app.route("/recipes/<id>", methods=("GET", "POST"))
def get_recipe(id: int) -> str:
    recipe = get(f"/recipes/{id}").json()
    ingredients = get(f"/recipes/{id}/ingredients").json()

    return render_template("recipe.html", recipe=recipe, ingredients=ingredients)


def recipe_from_form(form: ImmutableMultiDict) -> Tuple[dict, list]:
    name = form["name"]
    servings = form["servings"]
    method = form["method"]
    tags = form["tags"].strip()

    ingredient_keys = sorted(k for k in form if k.startswith("ingredient"))
    quantity_keys = sorted(k for k in form if k.startswith("quantity"))
    measure_keys = sorted(k for k in form if k.startswith("measure"))
    optional_keys = sorted(set(k for k in form if k.startswith("optional")))

    ingredients = [
        {
            "name": form[k1],
            "quantity": form[k2],
            "measure": form[k3],
            "optional": "on" in form.getlist(k4),
        }
        for k1, k2, k3, k4 in zip(
            ingredient_keys, quantity_keys, measure_keys, optional_keys
        )
    ]

    return {
        "name": name,
        "servings": servings,
        "method": method,
        "tags": tags,
    }, ingredients


@app.route("/add_recipe", methods=("GET", "POST"))
def add_recipe() -> str:
    if request.method == "POST":
        recipe, ingredients = recipe_from_form(request.form)

        db_recipe = post("/recipes", json=recipe).json()

        for ingredient in ingredients:
            db_ingredient = post("/ingredients", json=ingredient).json()

            if not (db_recipe.id and db_ingredient.id):
                abort(404)

            recipe_ingredient_data = {
                "recipe_id": db_recipe.id,
                "ingredient_id": db_ingredient.id,
                "quantity": ingredient["quantity"],
                "measure": ingredient["measure"],
                "optional": ingredient["optional"],
            }

            post(f"/recipes/{db_recipe.id}/ingredients", json=recipe_ingredient_data)

    return render_template("add_recipe.html")


@app.route("/mealplan", methods=("GET", "POST"))
def mealplan() -> str:
    return render_template("mealplan.html")


@app.route("/add_mealplans", methods=("GET", "POST"))
def add_mealplans() -> str:
    mps = get("/mealplans").json()

    if request.method == "POST":
        start = request.form["start_date"]
        end = request.form.get("end_date") or start  # default to start date

        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")

        meals = [
            dict(zip(("name", "servings"), row.split(";")))
            for row in request.form["meals"].splitlines()
        ]

        for d in datetime_range(start_dt, end_dt + timedelta(days=1)):
            for meal in meals:
                post("/mealplans", json={"date": d.date(), **meal})

    return render_template("add_mealplans.html", mealplans=mps)


@app.route("/shoppinglist", methods=("GET", "POST"))
def shopping_list() -> str:
    items = []
    if request.method == "POST":
        start = request.form["start_date"]
        end = request.form["end_date"]

        mps = get("/mealplans").json()

        chosen_mps = filter(lambda mp: start <= mp["date"] <= end, mps)  # type: ignore[arg-type,operator]

        # calculate how many servings are needed per recipe
        kf = lambda x: x["recipe_id"] or 0  # noqa: E731
        gb = groupby(sorted(chosen_mps, key=kf), key=kf)
        needed_servings = {
            recipe_id: sum(row["servings"] for row in rows) for recipe_id, rows in gb  # type: ignore[attr-defined]
        }

        # get recipes and their ingredients
        data = [
            {
                "recipe": get(f"/recipes/{i}").json(),
                "ingredients": get(f"/recipes/{i}/ingredients").json(),
                "servings": servings,
            }
            for i, servings in needed_servings.items()
        ]

        for d in data:
            if not (d["recipe"] and d["ingredients"]):
                continue

            scaling_factor = d["servings"] / d["recipe"]["servings"]  # type: ignore[operator,union-attr]

            items.append(
                {
                    "recipe": f"{d['recipe']['name']} ({float(d['servings']):g})",  # type: ignore[union-attr, arg-type]
                    "ingredients": [
                        {
                            "name": ing["ingredient"]["name"],
                            "measure": ing["measure"],
                            "quantity": scaling_factor * ing["quantity"],  # type: ignore[operator]
                            "optional": ing["optional"],
                        }
                        for ing in d["ingredients"]  # type: ignore[union-attr]
                    ],
                }
            )

    return render_template("shoppinglist.html", items=items)

from flask import Blueprint, jsonify, request
from backend.app import crud
from backend.app.dependencies import get_db

bp = Blueprint("recipes", __name__, url_prefix="/recipes")


@bp.get("/")
def read_recipes():
    return jsonify([x.as_dict() for x in crud.recipe.get_all(get_db())])


@bp.post("/")
def create_recipe():
    db = get_db()
    data = request.get_json()
    db_recipe = crud.recipe.create(
        db,
        name=data["name"],
        servings=data["servings"],
        method=data["method"],
        tags=data.get("tags", ""),
    )

    return jsonify(db_recipe.as_dict())


@bp.get("/<id>")
def read_recipe(id):
    db = get_db()
    return jsonify(crud.recipe.get(db, id).as_dict())


@bp.get("/<id>/ingredients")
def read_recipe_ingredients(id):
    db = get_db()
    return jsonify(crud.recipe.get_ingredients(db, id).as_dict())


@bp.post("/<id>/ingredients")
def create_recipe_ingredient(id):
    db = get_db()
    data = request.get_json()
    return crud.recipe.add_ingredient(
        db,
        recipe_id=id,
        ingredient_id=data["ingredient_id"],
        quantity=data["quantity"],
        measure=data["measure"],
    ).as_dict()

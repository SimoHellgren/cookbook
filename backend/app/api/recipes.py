from flask import Blueprint, Response, abort, jsonify, request
from backend.app import crud
from backend.app.dependencies import get_db

bp = Blueprint("recipes", __name__, url_prefix="/recipes")


@bp.get("/")
def read_recipes() -> Response:
    return jsonify([x.as_dict() for x in crud.recipe.get_all(get_db())])


@bp.post("/")
def create_recipe() -> Response:
    db = get_db()
    data = request.get_json()
    if not data:
        return jsonify({})

    db_recipe = crud.recipe.create(
        db,
        name=data["name"],
        servings=data["servings"],
        method=data["method"],
        tags=data.get("tags", ""),
    )

    return jsonify(db_recipe.as_dict())


@bp.get("/<id>")
def read_recipe(id: int) -> Response:
    db = get_db()
    db_recipe = crud.recipe.get(db, id)
    if db_recipe:
        return jsonify(db_recipe.as_dict())

    else:
        abort(404)


@bp.get("/<id>/ingredients")
def read_recipe_ingredients(id: int) -> Response:
    db = get_db()
    return jsonify([i.as_dict() for i in crud.recipe.get_ingredients(db, id)])


@bp.post("/<id>/ingredients")
def create_recipe_ingredient(id: int) -> Response:
    db = get_db()
    data = request.get_json()
    if not data:
        abort(404)

    return jsonify(
        crud.recipe.add_ingredient(
            db,
            recipe_id=id,
            ingredient_id=data["ingredient_id"],
            quantity=data["quantity"],
            measure=data["measure"],
            optional=data["optional"],
        ).as_dict()
    )

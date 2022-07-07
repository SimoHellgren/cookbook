from flask import Blueprint, jsonify
from backend.app import crud
from backend.app.dependencies import get_db

bp = Blueprint("recipe_ingredients", __name__, url_prefix="/recipe_ingredients")


@bp.get("/")
def read_recipe_ingredients():
    db = get_db()
    return jsonify([x.as_dict() for x in crud.recipe_ingredient.get_all(db)])

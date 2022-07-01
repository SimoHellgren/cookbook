from flask import Blueprint, jsonify, request
from backend import crud

bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@bp.get("/")
def read_ingredients():
    return jsonify(crud.ingredient.get_all())


@bp.post("/")
def create_ingredient():
    data = request.get_json()

    db_ingredient = crud.ingredient.create(name=data["name"])

    return jsonify(db_ingredient)

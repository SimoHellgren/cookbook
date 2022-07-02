from flask import Blueprint, jsonify, request
from backend import crud
from backend.dependencies import get_db

bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@bp.get("/")
def read_ingredients():
    db = get_db()
    return jsonify([x.as_dict() for x in crud.ingredient.get_all(db)])


@bp.post("/")
def create_ingredient():
    db = get_db()
    data = request.get_json()

    db_ingredient = crud.ingredient.create(db, name=data["name"])

    return jsonify(db_ingredient.as_dict())

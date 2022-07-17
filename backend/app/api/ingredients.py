from flask import Blueprint, abort, jsonify, request, Response
from backend.app import crud
from backend.app.dependencies import get_db
from backend.app.schemas.ingredient import IngredientCreate


bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@bp.get("/")
def read_ingredients() -> Response:
    db = get_db()
    return jsonify([x.as_dict() for x in crud.ingredient.get_many(db)])


@bp.post("/")
def create_ingredient() -> Response:
    db = get_db()
    data = request.get_json()

    if not data:
        abort(404)

    data_in = IngredientCreate(name=data["name"])

    db_ingredient = crud.ingredient.create(db=db, obj_in=data_in)

    return jsonify(db_ingredient.as_dict())

from flask import Blueprint, jsonify, request
from backend import crud
from backend.dependencies import get_db

bp = Blueprint("mealplans", __name__, url_prefix="/mealplans")


@bp.get("/")
def read_mealpans():
    db = get_db()
    return jsonify([x.as_dict() for x in crud.mealplan.get_all(db)])


@bp.get("/<id>")
def read_mealplan(id):
    db = get_db()
    return jsonify(crud.mealplan.get(db, id).as_dict())


@bp.post("/")
def create_mealplan():
    db = get_db()
    data = request.get_json()
    db_mealplan = crud.mealplan.create(
        db, date=data["date"], name=data["name"], servings=data["servings"]
    ).as_dict()

    return jsonify(db_mealplan)


@bp.put("/<id>")
def update_mealplan(id):
    db = get_db()
    data = request.get_json()
    db_mealplan = crud.mealplan.update(db, **data)

    return db_mealplan.as_dict()

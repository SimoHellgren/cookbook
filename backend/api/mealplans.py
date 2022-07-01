from flask import Blueprint, jsonify, request
from backend import crud

bp = Blueprint("mealplans", __name__, url_prefix="/mealplans")


@bp.get("/")
def read_mealpans():
    return jsonify(crud.mealplan.get_all())


@bp.get("/<id>")
def read_mealplan(id):
    return jsonify(crud.mealplan.get(id))


@bp.post("/")
def create_mealplan():
    data = request.get_json()
    db_mealplan = crud.mealplan.create(
        date=data["date"], name=data["name"], servings=data["servings"]
    )

    return jsonify(db_mealplan)


@bp.put("/<id>")
def update_mealplan(id):
    data = request.get_json()
    db_mealplan = crud.mealplan.update(**data)

    return db_mealplan

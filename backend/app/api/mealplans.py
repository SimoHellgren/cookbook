from flask import Blueprint, Response, abort, jsonify, request
from backend.app import crud
from backend.app.dependencies import get_db
from backend.app.schemas.mealplan import MealplanCreate, MealplanUpdate

bp = Blueprint("mealplans", __name__, url_prefix="/mealplans")


@bp.get("/")
def read_mealpans() -> Response:
    db = get_db()
    return jsonify([x.as_dict() for x in crud.mealplan.get_many(db)])


@bp.get("/<id>")
def read_mealplan(id: int) -> Response:
    db = get_db()
    db_obj = crud.mealplan.get(db, id)
    if not db_obj:
        abort(404)

    return jsonify(db_obj.as_dict())


@bp.post("/")
def create_mealplan() -> Response:
    db = get_db()
    data = request.get_json()
    if not data:
        abort(404)

    data_in = MealplanCreate(
        date=data["date"], name=data["name"], servings=data["servings"]
    )
    db_mealplan = crud.mealplan.create(db=db, obj_in=data_in)

    if db_mealplan:
        return jsonify(db_mealplan.as_dict())

    return jsonify({})


@bp.put("/<id>")
def update_mealplan(id: int) -> Response:
    db = get_db()
    data = request.get_json()
    db_obj = crud.mealplan.get(db, id)

    if not (data and db_obj):
        abort(404)

    data_in = MealplanUpdate(
        id=data["id"],
        name=data["name"],
        date=data["date"],
        servings=data["servings"],
        recipe_id=data["recipe_id"],
    )

    db_mealplan = crud.mealplan.update(
        db=db,
        db_obj=db_obj,
        obj_in=data_in,
    )

    if db_mealplan:
        return jsonify(db_mealplan.as_dict())

    return jsonify({})

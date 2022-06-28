from flask import Blueprint, jsonify, request
import db

bp = Blueprint('mealplans', __name__, url_prefix='/mealplans')


@bp.get('/')
def read_mealpans():
    return jsonify(db.get_mealplans())


@bp.post('/')
def create_mealplan():
    data = request.get_json()
    db_mealplan = db.create_mealplan(
        date=data['date'],
        name=data['name'],
        servings=data['servings']
    )

    return jsonify(db_mealplan)

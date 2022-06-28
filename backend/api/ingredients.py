from flask import Blueprint, jsonify, request
import backend.db as db
bp = Blueprint('ingredients', __name__, url_prefix='/ingredients')


@bp.get('/')
def read_ingredients():
    return jsonify(db.get_ingredients())


@bp.post('/')
def create_ingredient():
    data = request.get_json()

    db_ingredient = db.create_ingredient(
        name=data['name']
    )

    return jsonify(db_ingredient)

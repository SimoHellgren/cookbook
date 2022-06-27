from flask import Blueprint, jsonify, request
import db
bp = Blueprint('recipe', __name__, url_prefix='/recipe')


@bp.get('/')
def read_recipes():
    return jsonify(db.get_recipes())


@bp.post('/')
def create_recipe():
    data = request.get_json()
    db_recipe = db.create_recipe(
        name=data['name'],
        servings=data['servings'],
        method=data['method'],
        tags=data.get('tags', '')
    )

    return db_recipe


@bp.get('/<id>')
def read_recipe(id):
    return jsonify(db.get_recipe_by_id(id))

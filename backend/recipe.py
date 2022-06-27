from flask import Blueprint, jsonify
import db
bp = Blueprint('recipe', __name__, url_prefix='/recipe')


@bp.get('/')
def read_recipes():
    return jsonify(db.get_recipes())


@bp.get('/<id>')
def read_recipe(id):
    return jsonify(db.get_recipe_by_id(id))

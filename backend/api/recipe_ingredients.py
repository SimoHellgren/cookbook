from flask import Blueprint, jsonify
import backend.db as db
bp = Blueprint('recipe_ingredients', __name__, url_prefix='/recipe_ingredients')


@bp.get('/')
def read_recipe_ingredients():
    return jsonify(db.get_recipe_ingredients())

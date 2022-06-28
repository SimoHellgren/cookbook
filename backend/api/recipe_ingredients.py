from flask import Blueprint, jsonify
from backend import crud
bp = Blueprint('recipe_ingredients', __name__, url_prefix='/recipe_ingredients')


@bp.get('/')
def read_recipe_ingredients():
    return jsonify(crud.recipe_ingredient.get_all())

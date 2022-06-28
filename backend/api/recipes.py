from flask import Blueprint, jsonify, request
from backend import crud
bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.get('/')
def read_recipes():
    return jsonify(crud.recipe.get_all())


@bp.post('/')
def create_recipe():
    data = request.get_json()
    db_recipe = crud.recipe.create(
        name=data['name'],
        servings=data['servings'],
        method=data['method'],
        tags=data.get('tags', '')
    )

    return jsonify(db_recipe)


@bp.get('/<id>')
def read_recipe(id):
    return jsonify(crud.recipe.get(id))


@bp.get('/<id>/ingredients')
def read_recipe_ingredients(id):
    return jsonify(crud.recipe.get_ingredients(id))


@bp.post('/<id>/ingredients')
def create_recipe_ingredient(id):
    data = request.get_json()
    return crud.recipe.add_ingredient(
        recipe_id=id,
        ingredient_id=data['ingredient_id'],
        quantity=data['quantity'],
        measure=data['measure']
    )

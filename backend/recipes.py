from flask import Blueprint, jsonify, request
import db
bp = Blueprint('recipes', __name__, url_prefix='/recipes')


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

    return jsonify(db_recipe)


@bp.get('/<id>')
def read_recipe(id):
    return jsonify(db.get_recipe_by_id(id))


@bp.get('/<id>/ingredients')
def read_recipe_ingredients(id):
    return jsonify(db.get_recipe_ingredients_by_recipe_id(id))


@bp.post('/<id>/ingredients')
def create_recipe_ingredient(id):
    data = request.get_json()
    return db.create_recipe_ingredient(
        recipe_id=id,
        ingredient_id=data['ingredient_id'],
        quantity=data['quantity'],
        measure=data['measure']
    )

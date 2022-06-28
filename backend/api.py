from flask import Blueprint
from . import recipes
from . import ingredients
from . import recipe_ingredients

bp = Blueprint('api', __name__, url_prefix='/api')

bp.register_blueprint(recipes.bp)
bp.register_blueprint(ingredients.bp)
bp.register_blueprint(recipe_ingredients.bp)


@bp.get('/')
def test():
    return "hello there"

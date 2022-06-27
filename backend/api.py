from flask import Blueprint
from . import recipe
from . import ingredient

bp = Blueprint('api', __name__, url_prefix='/api')

bp.register_blueprint(recipe.bp)
bp.register_blueprint(ingredient.bp)


@bp.get('/')
def test():
    return "hello there"

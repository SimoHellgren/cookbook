from flask import Blueprint
from . import recipe

bp = Blueprint('api', __name__, url_prefix='/api')

bp.register_blueprint(recipe.bp)


@bp.get('/')
def test():
    return "hello there"

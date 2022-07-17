from backend.app.crud.base import CRUDBase
from backend.app.models import Ingredient
from backend.app.schemas.ingredient import IngredientCreate, IngredientUpdate


ingredient = CRUDBase[Ingredient, IngredientCreate, IngredientUpdate](Ingredient)

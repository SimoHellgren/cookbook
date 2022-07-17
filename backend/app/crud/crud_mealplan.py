from backend.app.crud.base import CRUDBase
from backend.app.models import Mealplan
from backend.app.schemas.mealplan import MealplanCreate, MealplanUpdate

mealplan = CRUDBase[Mealplan, MealplanCreate, MealplanUpdate](Mealplan)

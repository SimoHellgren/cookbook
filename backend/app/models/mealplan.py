from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Enum
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base
from backend.app.enums import MealplanState
from backend.app.models import Recipe


class Mealplan(Base):
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    name = Column(String, nullable=False)
    servings = Column(Numeric)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))
    state = Column(Enum(MealplanState), default=MealplanState.open)

    recipe: Recipe = relationship(Recipe, back_populates="mealplans", uselist=False)

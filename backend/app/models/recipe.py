from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from backend.app.models import RecipeIngredient, Mealplan


class Recipe(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    servings = Column(Numeric)
    method = Column(String)
    tags = Column(String)
    source = Column(String)

    ingredients: List["RecipeIngredient"] = relationship(
        "RecipeIngredient", back_populates="recipe", uselist=True
    )
    mealplans: List["Mealplan"] = relationship(
        "Mealplan", back_populates="recipe", uselist=True
    )

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.app.models import Recipe, Ingredient  # noqa: F401


class RecipeIngredient(Base):
    # override default due to wanting the underscore
    __tablename__ = "recipe_ingredient"  # type: ignore[assignment]

    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    quantity = Column(Numeric)
    measure = Column(String)
    optional = Column(Boolean, nullable=False, default=False)

    recipe = relationship("Recipe", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="recipes")

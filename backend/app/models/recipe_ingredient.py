from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.db.base_class import Base
from backend.app.models import Recipe, Ingredient


class RecipeIngredient(Base):
    # override default due to wanting the underscore
    __tablename__ = "recipe_ingredient"  # type: ignore[assignment]

    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    quantity = Column(Numeric)
    measure = Column(String)
    optional = Column(Boolean, nullable=False, default=False)
    position = Column(Integer, nullable=False)

    recipe: Recipe = relationship(Recipe, back_populates="ingredients", uselist=False)
    ingredient: Ingredient = relationship(
        Ingredient, back_populates="recipes", uselist=False, lazy="subquery"
    )

    __table_args__ = (
        UniqueConstraint("recipe_id", "position", name="recipeid_position_unique"),
    )

from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from backend.db.base_class import Base


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredient'  # override default behavior due to _

    recipe_id = Column(Integer, ForeignKey("recipe.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    quantity = Column(Numeric)
    measure = Column(String)

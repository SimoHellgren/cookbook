from sqlalchemy import Column, Integer, String, ForeignKey
from backend.app.db.base_class import Base


class Comment(Base):
    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))

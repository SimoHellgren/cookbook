from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    id: int
    comment: str
    recipe_id: id
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    """For use as API response model"""

    class Config:
        orm_mode = True

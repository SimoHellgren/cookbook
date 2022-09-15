from typing import Optional
from pydantic import BaseModel


class CommentBase(BaseModel):
    comment: str
    recipe_id: int
    parent_id: Optional[int] = None
    author: Optional[str]


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    id: int


class Comment(CommentBase):
    """For use as API response model"""
    id: int

    class Config:
        orm_mode = True

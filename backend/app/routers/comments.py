from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app import crud
from backend.app.schemas.comment import Comment, CommentCreate, CommentUpdate
from backend.app.dependencies import get_db


router = APIRouter(prefix="/comments")


@router.get("/", response_model=list[Comment])
def get_all(db: Session = Depends(get_db)) -> Any:
    return crud.comment.get_many(db)


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create(comment: CommentCreate, db: Session = Depends(get_db)) -> Any:
    return crud.comment.create(db, comment)


@router.put("/{comment_id}", response_model=Comment)
def update(
    comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)
) -> Any:
    db_obj = crud.comment.get(db, comment_id)

    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return crud.comment.update(db, db_obj, comment)


@router.delete("/{comment_id}", response_model=Comment)
def delete(comment_id: int, db: Session = Depends(get_db)) -> Any:
    return crud.comment.remove(db, comment_id)

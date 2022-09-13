from backend.app.crud.base import CRUDBase
from backend.app.models import Comment
from backend.app.schemas.comment import CommentCreate, CommentUpdate

comment = CRUDBase[Comment, CommentCreate, CommentUpdate](Comment)

from typing import Any, Dict
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    # generate tablename automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()  # type: ignore[attr-defined]

    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore[attr-defined]

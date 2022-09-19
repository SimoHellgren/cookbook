from datetime import datetime
from typing import Any, Dict
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime, text

_utc_timestamp = text("(now() at time zone 'utc')")


@as_declarative()
class Base:
    created = Column(DateTime, server_default=_utc_timestamp)
    updated = Column(
        DateTime,
        server_default=_utc_timestamp,
        onupdate=datetime.utcnow,
    )

    # generate tablename automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore[attr-defined]

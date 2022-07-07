from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    # generate tablename automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

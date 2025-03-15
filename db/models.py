from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


class TableModel(Base):
    title: Mapped[str] = mapped_column(String(250))
    url: Mapped[str] = mapped_column(String(250))
    xpath: Mapped[str] = mapped_column(String(250))

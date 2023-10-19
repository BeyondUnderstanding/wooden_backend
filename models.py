from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class BaseSchema(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class Admin(BaseSchema):

    login: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str]


class Game(BaseSchema):

    title: Mapped[str] = mapped_column(String(50))  # Lenght may be greater than 50?
    description: Mapped[str]
    price: Mapped[float]
    is_deleted: Mapped[Optional[bool]] = mapped_column(default=False)

    attributes: Mapped[List["GameAttribute"]] = relationship(back_populates='game')
    books: Mapped[List["Book"]] = relationship(back_populates='game')
    images: Mapped[List["Image"]] = relationship(back_populates='game')


class GameAttribute(BaseSchema):

    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='attributes')

    name: Mapped[str]
    value: Mapped[str]
    is_main: Mapped[Optional[bool]] = mapped_column(default=False)
    icon: Mapped[Optional[str]]


class Book(BaseSchema):

    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='books')
    date: Mapped[datetime]
    client_name: Mapped[str]
    client_phone: Mapped[str]
    is_payed: Mapped[Optional[bool]] = mapped_column(default=False)
    is_refunded: Mapped[Optional[bool]] = mapped_column(default=False)
    is_canceled: Mapped[bool] = mapped_column(default=False)


class Image(BaseSchema):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='images')

    link: Mapped[str]
    priority: Mapped[int] = mapped_column(default=0)

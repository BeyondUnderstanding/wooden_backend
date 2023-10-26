from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

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
    sales_count: Mapped[Optional[int]] = mapped_column(default=0)

    attributes: Mapped[List["GameAttribute"]] = relationship(back_populates='game')
    books: Mapped[List["Book"]] = relationship(back_populates='game')
    images: Mapped[List["Image"]] = relationship(back_populates='game')
    books: Mapped[List["GameToBook"]] = relationship(back_populates='game')


class GameAttribute(BaseSchema):

    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='attributes')

    name: Mapped[str]
    value: Mapped[str]
    is_main: Mapped[Optional[bool]] = mapped_column(default=False)
    icon: Mapped[Optional[str]]


class GameToBook(BaseSchema):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    game_price_before: Mapped[float]
    game_price_after: Mapped[float]

    game: Mapped[Game] = relationship(back_populates='books')
    book: Mapped['Book'] = relationship(back_populates='games')


class Book(BaseSchema):

    date: Mapped[datetime]
    client_name: Mapped[str]
    client_phone: Mapped[str]
    is_payed: Mapped[Optional[bool]] = mapped_column(default=False)
    is_refunded: Mapped[Optional[bool]] = mapped_column(default=False)
    is_canceled: Mapped[bool] = mapped_column(default=False)
    legal_id: Mapped[str] = mapped_column(String(11))
    has_manager: Mapped[Optional[bool]] = mapped_column(default=False)
    managers_count: Mapped[Optional[int]] = mapped_column(default=0)
    total_price: Mapped[float]


    games: Mapped[List[GameToBook]] = relationship(back_populates='book')


    @validates('legal_id')
    def validate_legal_id(self, key, legal_id) -> str:
        if len(legal_id)<11:
            raise ValueError('legal_id too short')
        return legal_id



class Image(BaseSchema):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='images')

    link: Mapped[str]
    priority: Mapped[int] = mapped_column(default=0)
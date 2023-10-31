from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, ForeignKey, select, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, declared_attr, DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass


class Base(DeclarativeBase):
    __abstract__ = True
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class Admin(Base):
    login: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str]


class Game(Base):
    title: Mapped[str] = mapped_column(String(50))  # Length may be greater than 50?
    description: Mapped[str]
    price: Mapped[float]
    is_deleted: Mapped[Optional[bool]] = mapped_column(default=False)
    sales_count: Mapped[Optional[int]] = mapped_column(default=0)

    attributes: Mapped[List["GameAttribute"]] = relationship(back_populates='game')
    images: Mapped[List["Image"]] = relationship(back_populates='game')
    books: Mapped[List["GameToBook"]] = relationship(back_populates='game')
    in_baskets: Mapped[List['BasketItem']] = relationship(back_populates='game')
    as_bonus: Mapped[List['Book']] = relationship(back_populates='bonus_game')
    occupied_dates: Mapped[List['OccupiedDateTime']] = relationship(back_populates='game')

    def check_available(self, start_date, end_date):
        if not start_date or not end_date:
            return True
        from db.database import get_db
        from modules.client.basket.utils import calculate_delta
        delta = calculate_delta(start_date, end_date)
        session = next(get_db())
        availability = session.scalar(select(OccupiedDateTime).where(
            and_(
                OccupiedDateTime.game_id == self.id,
                OccupiedDateTime.datetime.in_(delta)
                 )
        ).limit(1))

        return not bool(availability)


class GameAttribute(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='attributes')

    name: Mapped[str]
    value: Mapped[str]
    is_main: Mapped[Optional[bool]] = mapped_column(default=False)
    icon: Mapped[Optional[str]]


class GameToBook(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    game_price_before: Mapped[float]
    game_price_after: Mapped[float]

    game: Mapped[Game] = relationship(back_populates='books')
    book: Mapped['Book'] = relationship(back_populates='games')
    occupied_dates: Mapped[List['OccupiedDateTime']] = relationship(back_populates='game_to_book')


class Book(Base):
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    client_name: Mapped[str]
    client_phone: Mapped[str]
    client_email: Mapped[str]
    is_payed: Mapped[Optional[bool]] = mapped_column(default=False)
    is_refunded: Mapped[Optional[bool]] = mapped_column(default=False)
    is_canceled: Mapped[bool] = mapped_column(default=False)
    legal_id: Mapped[str] = mapped_column(String(11))
    has_manager: Mapped[Optional[bool]] = mapped_column(default=False)
    managers_count: Mapped[Optional[int]] = mapped_column(default=0)
    total_price: Mapped[float]
    has_bonus_game: Mapped[Optional[bool]] = mapped_column(default=False)
    bonus_game_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Game.id), default=None)
    test_field: Mapped[bool] = mapped_column(default=False)  # to be deleted

    games: Mapped[List[GameToBook]] = relationship(back_populates='book')
    bonus_game: Mapped[Game] = relationship(back_populates='as_bonus')

    @validates('legal_id')
    def validate_legal_id(self, key, legal_id) -> str:  # noqa
        if len(legal_id) < 11:
            raise ValueError('legal_id too short')
        return legal_id


class Basket(Base):
    user_uuid: Mapped[str]
    start_date: Mapped[Optional[datetime]] = mapped_column(default=None)
    end_date: Mapped[Optional[datetime]] = mapped_column(default=None)

    items: Mapped[List['BasketItem']] = relationship(back_populates='basket')


class BasketItem(Base):
    basket_id: Mapped[int] = mapped_column(ForeignKey(Basket.id))
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))

    basket: Mapped[Basket] = relationship(back_populates='items')
    game: Mapped[Game] = relationship(back_populates='in_baskets')


class Image(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='images')

    link: Mapped[str]
    priority: Mapped[int] = mapped_column(default=0)


class OccupiedDateTime(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game_to_book_id: Mapped[int] = mapped_column(ForeignKey(GameToBook.id))

    datetime: Mapped[datetime]

    game: Mapped[Game] = relationship(back_populates='occupied_dates')
    game_to_book: Mapped[GameToBook] = relationship(back_populates='occupied_dates')

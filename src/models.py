from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, ForeignKey, select, and_, func, or_
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, declared_attr, DeclarativeBase
from src.modules.client.basket.schema import PaymentMethod


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

    def check_available(self, delta: List[datetime]):
        if not delta:
            return True
        from src.db.database import get_db

        # Very bad! In current logic order must be from same year-month-day,
        # but i think(impressive!), its universal solution

        years = set(d.year for d in delta)
        months = set(d.month for d in delta)
        days = set(d.day for d in delta)

        session = next(get_db())
        availability = session.scalar(select(OccupiedDateTime).where(
            and_(
                or_(
                    OccupiedDateTime.game_id == self.id,
                    OccupiedDateTime.game_id == None  # noqa
                ),
                func.extract('year', OccupiedDateTime.datetime).in_(years),
                func.extract('month', OccupiedDateTime.datetime).in_(months),
                func.extract('day', OccupiedDateTime.datetime).in_(days)
            )
        ).limit(1))

        return not bool(availability)


class GameAttribute(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    game: Mapped[Game] = relationship(back_populates='attributes')

    name: Mapped[str]
    value: Mapped[str]
    is_main: Mapped[Optional[bool]] = mapped_column(default=False)


class GameToBook(Base):
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id))
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    game_price_before: Mapped[float]
    game_price_after: Mapped[float]

    game: Mapped[Game] = relationship(back_populates='books')
    book: Mapped['Book'] = relationship(back_populates='games')
    occupied_dates: Mapped[List['OccupiedDateTime']] = relationship(back_populates='game_to_book')


class Book(Base):
    user_uuid: Mapped[str]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]
    client_name: Mapped[str]
    client_phone: Mapped[str]
    client_email: Mapped[str]

    payment_method: Mapped[PaymentMethod] = mapped_column(server_default='card')
    is_payed: Mapped[Optional[bool]] = mapped_column(default=False)
    is_refunded: Mapped[Optional[bool]] = mapped_column(default=False)
    is_canceled: Mapped[bool] = mapped_column(default=False)
    is_prepayment: Mapped[bool] = mapped_column(server_default='0')
    prepayment_done: Mapped[bool] = mapped_column(server_default='0')

    legal_id: Mapped[str] = mapped_column(String(11))
    has_manager: Mapped[Optional[bool]] = mapped_column(default=False)
    managers_count: Mapped[Optional[int]] = mapped_column(default=0)
    total_price: Mapped[float]
    has_bonus_game: Mapped[Optional[bool]] = mapped_column(default=False)
    bonus_game_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Game.id), default=None)
    delivery_address: Mapped[str]
    extra: Mapped[Optional[str]]
    total_hours: Mapped[int] = mapped_column(server_default='0')

    games: Mapped[List[GameToBook]] = relationship(back_populates='book')
    bonus_game: Mapped[Game] = relationship(back_populates='as_bonus')
    messages: Mapped[List['Message']] = relationship(back_populates='book')

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
    game_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Game.id))
    game_to_book_id: Mapped[Optional[int]] = mapped_column(ForeignKey(GameToBook.id))

    datetime: Mapped[datetime]

    game: Mapped[Game] = relationship(back_populates='occupied_dates')
    game_to_book: Mapped[GameToBook] = relationship(back_populates='occupied_dates')


class Config(Base):
    key: Mapped[str]
    value: Mapped[str]


# class Payment(Base):
#     order_id: Mapped[int]
#

class Message(Base):
    book_id: Mapped[int] = mapped_column(ForeignKey(Book.id))
    phone_number: Mapped[str]
    message: Mapped[str]
    is_delivered: Mapped[bool]
    sent_at: Mapped[datetime]

    book: Mapped[Book] = relationship(back_populates='messages')

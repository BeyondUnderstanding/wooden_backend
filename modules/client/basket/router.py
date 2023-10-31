import datetime
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from modules.client.basket.schema import AddToBasketSchema, BasketItemWithShortInfo, CreateBooking, UpdateBasketDates, \
    MinRequirementsException, DatesException, EmptyBasketException
from modules.client.basket.utils import calculate_order, calculate_hours, calculate_delta
from modules.client.games.schema import GameSchema
from modules.client.games.utils import populate_adapter
from modules.schema import require_uuid, UpdateObjectSchema
from db.database import get_db
from modules.schema import CreateObjectSchema, DeletedObjectSchema
from models import Basket, BasketItem, Game, Book, GameToBook, OccupiedDateTime

basket = APIRouter(prefix='/basket', tags=['Basket'])


def check_basket_exist(uuid: str, session: Session):
    if not session.scalar(select(Basket).where(Basket.user_uuid == uuid)):
        session.add(Basket(user_uuid=uuid))  # noqa
        session.commit()


@basket.get('', response_model=List[GameSchema])
async def get_items(session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    basket_info = session.scalar(select(Basket).where(
        Basket.user_uuid == uuid
    ))
    items = session.scalars(select(BasketItem).where(
        Basket.user_uuid == uuid
    ))
    populate = [populate_adapter(obj.game, basket_info.start_date, basket_info.end_date) for obj in items]
    return populate


@basket.post('', response_model=CreateObjectSchema)
async def add_item(data: AddToBasketSchema, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    # todo: add time collisions check
    check_basket_exist(uuid, session)
    game = session.get(Game, data.id)
    basket_obj = session.scalar(select(Basket).where(Basket.user_uuid == uuid))
    if not game:
        raise HTTPException(status_code=400, detail="Id is not exist")

    new_bi = BasketItem(basket_id=basket_obj.id,  # noqa
                        game_id=game.id)  # noqa
    session.add(new_bi)
    session.commit()
    return CreateObjectSchema(id=new_bi.id)


@basket.delete('', response_model=DeletedObjectSchema)
async def delete_item(id: int, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    bi_obj = session.scalar(select(BasketItem).where(
        and_(BasketItem.game_id == id, Basket.user_uuid == uuid)
    ))
    if not bi_obj:
        raise HTTPException(status_code=400, detail='Not found')

    session.delete(bi_obj)
    session.commit()
    return DeletedObjectSchema(id=bi_obj.game_id)


@basket.patch('', response_model=UpdateObjectSchema)
async def update_basket(data: UpdateBasketDates, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    basket_obj = session.scalar(select(Basket).where(Basket.user_uuid == uuid))
    basket_obj.start_date = data.start_date
    basket_obj.end_date = data.end_date
    session.add(basket_obj)
    session.commit()
    return UpdateObjectSchema(id=basket_obj.id)


@basket.post('/create_order', response_model=CreateObjectSchema)
async def create_order(data: CreateBooking, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    basket_obj = session.scalar(select(Basket).where(
        Basket.user_uuid == uuid
    ))
    basket_items: List[BasketItem] = basket_obj.items

    if not basket_obj.start_date or not basket_obj.end_date:
        raise HTTPException(status_code=400, detail='Dates are invalid')
    if calculate_hours(basket_obj) < 3:
        raise HTTPException(status_code=400, detail='Minimum requirements for the order are not met')
    if not basket_items:
        raise HTTPException(status_code=400, detail='Basket empty')

    occupied_datetimes = calculate_delta(basket_obj.start_date, basket_obj.end_date)
    for obj in basket_items:
        if session.scalar(select(OccupiedDateTime).where(
            and_(
                OccupiedDateTime.datetime.in_(occupied_datetimes),
                OccupiedDateTime.game_id == obj.game_id
            )
        ).limit(1)):
            raise HTTPException(status_code=400, detail=f'Game {obj.game_id} unavailable for booking')

    discount, managers, bonus_game = calculate_order(basket_items, basket_obj)
    games = session.scalars(select(Game).where(
        Game.id.in_([o.game.id for o in basket_items])
    ))
    gamestobook = []
    for g in games:
        gamestobook.append(GameToBook(
            game_id=g.id,
            game_price_before=g.price,
            game_price_after=g.price / 100 * discount
        ))
    total = sum([g.game_price_after for g in gamestobook])

    book = Book(
        start_date=basket_obj.start_date,
        end_date=basket_obj.end_date,
        client_name=data.client_name,
        client_phone=data.client_phone,
        client_email=data.client_email,
        legal_id=data.legal_id,
        has_manager=bool(managers),
        managers_count=managers,
        has_bonus_game=bonus_game,
        bonus_game_id=None,
        total_price=total
    )

    session.add(book)
    session.commit()

    for g in gamestobook:
        g.book_id = book.id

    session.add_all(gamestobook)
    session.commit()

    occupied_objs = []

    for g in gamestobook:
        for date in occupied_datetimes:
            occupied_objs.append(
                OccupiedDateTime(
                    game_id=g.game_id,
                    game_to_book_id=g.id,
                    datetime=date
                )
            )
    session.add_all(occupied_objs)
    session.commit()

    return CreateObjectSchema(id=book.id)

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models import Basket, BasketItem, Game, Book, GameToBook, OccupiedDateTime
from src.modules.client.basket.schema import AddToBasketSchema, CreateBooking, UpdateBasketDates, \
    CreateOrderOK
from src.modules.client.basket.utils import calculate_order, calculate_hours, calculate_delta
from src.modules.client.games.schema import GameSchema
from src.modules.client.games.utils import populate_adapter
from src.modules.schema import CreateObjectSchema, DeletedObjectSchema
from src.modules.schema import require_uuid, UpdateObjectSchema
from paymentwall import Paymentwall, Product, Widget
from math import ceil

basket = APIRouter(prefix='/basket', tags=['Basket'])


Paymentwall.set_api_type(Paymentwall.API_GOODS)
Paymentwall.set_app_key('')
Paymentwall.set_secret_key('')


def check_basket_exist(uuid: str, session: Session):
    if not session.scalar(select(Basket).where(Basket.user_uuid == uuid)):
        try:
            session.add(Basket(user_uuid=uuid))  # noqa
            session.commit()
        except:
            session.rollback()


@basket.get('', response_model=List[GameSchema])
async def get_items(session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    basket_info = session.scalar(select(Basket).where(
        Basket.user_uuid == uuid
    ))
    items = basket_info.items
    populate = [populate_adapter(obj.game, basket_info.start_date, basket_info.end_date) for obj in items]

    return populate


@basket.post('', response_model=CreateObjectSchema)
async def add_item(data: AddToBasketSchema, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    game = session.get(Game, data.id)
    basket_obj = session.scalar(select(Basket).where(Basket.user_uuid == uuid))
    if not game:
        raise HTTPException(status_code=400, detail="Game not found")
    if session.scalar(select(BasketItem).where(
            and_(
                Basket.user_uuid == uuid,
                BasketItem.game_id == game.id
            )
    ).join(Basket)):
        raise HTTPException(status_code=400, detail='Game already in basket')
    try:
        new_bi = BasketItem(basket_id=basket_obj.id,  # noqa
                            game_id=game.id)  # noqa
        session.add(new_bi)
        session.commit()
        return CreateObjectSchema(id=new_bi.id)
    except:
        session.rollback()


@basket.delete('', response_model=DeletedObjectSchema)
async def delete_item(id: int, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    bi_obj = session.scalar(select(BasketItem).where(
        and_(BasketItem.game_id == id, Basket.user_uuid == uuid)
    ).join(Basket))
    if not bi_obj:
        raise HTTPException(status_code=400, detail='Not found')
    try:
        session.delete(bi_obj)
        session.commit()
        return DeletedObjectSchema(id=bi_obj.game_id)
    except:
        session.rollback()


@basket.patch('', response_model=UpdateObjectSchema)
async def update_basket(data: UpdateBasketDates, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    basket_obj = session.scalar(select(Basket).where(Basket.user_uuid == uuid))
    basket_obj.start_date = data.start_date
    basket_obj.end_date = data.end_date
    try:
        session.add(basket_obj)
        session.commit()
        return UpdateObjectSchema(id=basket_obj.id)
    except:
        session.rollback()


@basket.post('/create_order', response_model=CreateOrderOK)
async def create_order(data: CreateBooking, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    basket_obj = session.scalar(select(Basket).where(
        Basket.user_uuid == uuid
    ))
    basket_items: List[BasketItem] = basket_obj.items

    if not basket_obj.start_date or not basket_obj.end_date:
        raise HTTPException(status_code=400, detail='Dates are invalid')
    total_hours = calculate_hours(basket_obj)
    if total_hours < 3:
        raise HTTPException(status_code=400, detail='Minimum requirements for the order are not met')
    if not basket_items:
        raise HTTPException(status_code=400, detail='Basket empty')

    occupied_datetimes = calculate_delta(basket_obj.start_date, basket_obj.end_date)
    #
    game_ids = [obj.game_id for obj in basket_items]
    years = set(d.year for d in occupied_datetimes)
    months = set(d.month for d in occupied_datetimes)
    days = set(d.day for d in occupied_datetimes)

    g_id_list = session.scalars(select(OccupiedDateTime.game_id.distinct()).where(
        and_(
            OccupiedDateTime.game_id.in_(game_ids),
            func.extract('year', OccupiedDateTime.datetime).in_(years),
            func.extract('month', OccupiedDateTime.datetime).in_(months),
            func.extract('day', OccupiedDateTime.datetime).in_(days)
        )
    )).all()
    if g_id_list:
        raise HTTPException(status_code=400, detail=f'Games {[g for g in g_id_list]} unavailable for booking')

    discount, managers, bonus_game = calculate_order(basket_items, basket_obj)
    games = session.scalars(select(Game).where(
        Game.id.in_([o.game.id for o in basket_items])
    ))
    gamestobook = []
    for g in games:
        gamestobook.append(GameToBook(
            game_id=g.id,
            game_price_before=g.price,
            game_price_after=g.price * discount
        ))

    # Считаем сумму всех игр и умножаем на кол-во часов.
    # Округляем в бОльшую сторону, плюс, плюсуем 15 лари за доставку
    total = ceil(sum([g.game_price_after for g in gamestobook]) * total_hours) + 15

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

    try:
        session.add(book)
        session.flush()
    except:
        session.rollback()
        raise HTTPException(status_code=500, detail='Something went wrong')

    for g in gamestobook:
        g.book_id = book.id

    try:
        session.add_all(gamestobook)
        session.flush()
    except:
        session.rollback()
        raise HTTPException(status_code=500, detail='Something went wrong')

    occupied_objs = []
    try:
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
        for b_obj in basket_items:
            session.delete(b_obj)

        session.commit()

    except:
        session.rollback()
        raise HTTPException(status_code=500, detail='Something went wrong')

    # products = [Product(g.id, g.game_price_after, 'GEL', g.game.title)
    #             for g in gamestobook]
    # widget = Widget(
    #     uuid,
    #     'pw_1',
    #     products,
    #     {
    #         'email': book.client_email,
    #
    #     }
    # )
    return CreateOrderOK(checkout_url="https://google.com")

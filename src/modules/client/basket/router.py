from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.config import UNIPAY_SECRET, UNIPAY_MERCH_ID
from src.modules.client.basket.schema import AddToBasketSchema, CreateBooking, UpdateBasketDates, \
    CreateOrderOK, CreateOrderError
from src.modules.client.basket.utils import calculate_order, calculate_hours, calculate_delta
from src.modules.client.games.schema import GameSchema
from src.modules.client.games.utils import populate_adapter
from src.modules.schema import require_uuid, UpdateObjectSchema
from src.db.database import get_db
from src.modules.schema import CreateObjectSchema, DeletedObjectSchema
from src.models import Basket, BasketItem, Game, Book, GameToBook, OccupiedDateTime
from src.payments import OrderItem, UniPayClient, APIError

basket = APIRouter(prefix='/basket', tags=['Basket'])
unipay = UniPayClient(
    UNIPAY_SECRET,
    UNIPAY_MERCH_ID,
    '/v1/payments/success',
    '/v1/payments/cancel',
    '/v1/payments/callback'
)


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
    ).join(Basket))
    if not bi_obj:
        raise HTTPException(status_code=400, detail='Not found')

    session.delete(bi_obj)
    session.commit()
    return DeletedObjectSchema(id=bi_obj.game_id)


@basket.patch('', response_model=UpdateObjectSchema)
async def update_basket(data: UpdateBasketDates, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    basket_obj = session.scalar(select(Basket).where(Basket.user_uuid == uuid))
    basket_obj.start_date = data.start_date
    basket_obj.end_date = data.end_date
    session.add(basket_obj)
    session.commit()
    return UpdateObjectSchema(id=basket_obj.id)


@basket.post('/create_order', response_model=CreateOrderOK, responses={500: {'model': CreateOrderError}})
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
            game_price_after=g.price / 100 * discount
        ))
    total = round(sum([g.game_price_after for g in gamestobook]), 2)

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
    for b_obj in basket_items:
        session.delete(b_obj)

    session.commit()
    ####################
    #   Payments part
    ####################

    # order_items = [
    #     OrderItem.from_dict(
    #         {'price': g.game_price_after,
    #          'quantity': total_hours,
    #          'title': g.game.title,
    #          'description': g.game.description}
    #     ) for g in gamestobook
    # ]
    # unipay_data = unipay.create_order(book.id, uuid, book.total_price, 'Book at WoodenGames.ge', '', order_items)
    # if unipay_data.errorcode == APIError.OK:
    return CreateOrderOK(checkout_url="https://google.com")
    # else:
    #     content = CreateOrderError(error=unipay_data.errorcode).model_dump()
    #     print(content)
    #     return JSONResponse(
    #         status_code=500,
    #         content=content
    #     )



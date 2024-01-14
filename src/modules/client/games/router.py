import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, distinct, func, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from src.models import Game, Basket, OccupiedDateTime, BasketItem, Image
from src.db.database import get_db
from .schema import GameSchema, GameSchemaFull, OccupiedDateTimeSchema
from .utils import populate_adapter, populate_adapter_full
from src.modules.client.basket.router import check_basket_exist
from ...schema import require_uuid

client_games = APIRouter(prefix='/games', tags=['Games'])


@client_games.get('', response_model=List[GameSchema], description=
"""Возвращает список доступных к приобретению игр (not deleted), по умолчанию (если не заполнены
                  данные start_date, end_date) отдает is_available=True для каждого товара, если заполнены, 
                  отдает текущую доступность по дате""")
async def get_all(session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    games = session.scalars(select(Game).where(Game.is_deleted.is_not(True))
                            .join(Image)
                            .order_by(Game.id.asc())
                            .distinct(Game.id)
                            )
    current_basket = session.scalar(select(Basket).where(Basket.user_uuid == uuid))

    return [populate_adapter(game, current_basket.start_date, current_basket.end_date) for game in games]


@client_games.get('/featured', response_model=List[GameSchema],
                  description="Отдает 3 игры которые не находятся в корзине, сортирует по кол-во продаж asc")
async def get_featured(session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    check_basket_exist(uuid, session)
    current_basket_games = session.scalars(select(BasketItem.game_id)
                                           .where(Basket.user_uuid == uuid)
                                           .join(Basket)).all()
    featured = session.scalars(select(Game)
                               .where(
                                    and_(
                                        Game.is_deleted.is_not(True),
                                        Game.id.notin_(current_basket_games)
                                    )
                                )
                               .order_by(Game.sales_count.asc())
                               .limit(3))
    return [populate_adapter(g, None, None) for g in featured]


@client_games.get('/by_date', response_model=List[GameSchema])
async def get_by_date(start_date: datetime.datetime, end_date: datetime.datetime,
                      session: Session = Depends(get_db)):
    games_list = session.scalars(select(Game)
                                 .where(Game.is_deleted.is_not(True))
                                 )
    return_list = [populate_adapter(game, start_date, end_date) for game in games_list]
    return return_list


@client_games.get('/get', response_model=GameSchemaFull)
async def get_one(id: int, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    current_basket = check_basket_exist(uuid, session)
    game: Game | None = session.get(Game, id)
    if not game:
        return JSONResponse(status_code=404, content={'error': 'game not found'})

    # current_basket = session.scalar(select(Basket).where(Basket.user_uuid == uuid))

    return populate_adapter_full(game, current_basket.start_date, current_basket.end_date)


@client_games.get('/get_occupied_dates', response_model=List[datetime.date])
async def get_occupied_dates(session: Session = Depends(get_db)):
    dates = session.scalars(select(
        distinct(
            OccupiedDateTime.datetime
        )
    )
    )
    return set(str(d.date()) for d in dates)

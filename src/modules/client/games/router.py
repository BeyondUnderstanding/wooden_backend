import datetime
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, distinct, func
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from src.models import Game, Basket, OccupiedDateTime
from src.db.database import get_db
from .schema import GameSchema, GameSchemaFull, OccupiedDateTimeSchema
from .utils import populate_adapter, populate_adapter_full
from ...schema import require_uuid

client_games = APIRouter(prefix='/games', tags=['Games'])


@client_games.get('', response_model=List[GameSchema])
async def get_all(session: Session = Depends(get_db)):
    games = session.scalars(select(Game).where(Game.is_deleted.is_not(True)))

    return [populate_adapter(game, None, None) for game in games]


@client_games.get('/by_date', response_model=List[GameSchema])
async def get_by_date(start_date: datetime.datetime, end_date: datetime.datetime,
                      session: Session = Depends(get_db)):
    games_list = session.scalars(select(Game).where(Game.is_deleted.is_not(True)))
    return_list = [populate_adapter(game, start_date, end_date) for game in games_list]
    return return_list


@client_games.get('/get', response_model=GameSchemaFull)
async def get_one(id: int, session: Session = Depends(get_db), uuid: str = Depends(require_uuid)):
    game: Game | None = session.get(Game, id)

    if not game:
        return JSONResponse(status_code=404, content={'error': 'game not found'})

    current_basket = session.scalar(select(Basket).where(Basket.user_uuid == uuid))

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
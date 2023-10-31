import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import Session
from models import Game

from db.database import get_db
from .schema import GameSchema
from .utils import populate_adapter

client_games = APIRouter(prefix='/games')


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

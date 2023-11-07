from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models import Game
from .schema import GameSchema, GameSchemaWithAttributes, GameSchemaUpdate
from ..auth.router import access_security
from ...schema import CreateObjectSchema, UpdateObjectSchema, DeletedObjectSchema
from .attributes.router import attributes_router

games_router = APIRouter(prefix='/games')
games_router.include_router(attributes_router, tags=['Attributes'])


@games_router.post('', response_model=CreateObjectSchema, tags=['Games'])
async def create(data: GameSchema, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    new_game = Game(**data.model_dump())  # noqa
    session.add(new_game)
    session.commit()
    session.refresh(new_game)

    return {'id': new_game.id}


@games_router.get('', response_model=List[GameSchemaWithAttributes], tags=['Games'])
async def get(session: Session = Depends(get_db), auth: JwtAuthorizationCredentials = Security(access_security)):
    games = session.scalars(select(Game).where(Game.is_deleted == False).order_by(Game.id.asc()))  # noqa
    return games


@games_router.patch('', response_model=UpdateObjectSchema, tags=['Games'])
async def patch(data: GameSchemaUpdate, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    game = session.get(Game, data.id)

    for k, v in data.model_dump().items():
        if v is not None:
            setattr(game, k, v)

    session.add(game)
    session.commit()
    return {'id': game.id}


@games_router.delete('', response_model=DeletedObjectSchema, tags=['Games'])
async def delete(id: int, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    game = session.get(Game, id)
    game.is_deleted = True
    session.add(game)
    session.commit()
    return {'id': game.id}




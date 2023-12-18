from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models import Game, Config
from .schema import GameSchema, GameSchemaWithAttributes, GameSchemaUpdate, GameSchemaBasic
from ..auth.router import access_security
from ...schema import CreateObjectSchema, UpdateObjectSchema, DeletedObjectSchema
from .attributes.router import attributes_router

games_router = APIRouter(prefix='/games')
games_router.include_router(attributes_router, tags=['Attributes'])


@games_router.post('', response_model=CreateObjectSchema, tags=['AdminGames'])
async def create(data: GameSchema, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    new_game = Game(**data.model_dump())  # noqa
    session.add(new_game)
    session.commit()
    session.refresh(new_game)

    return {'id': new_game.id}


def game_with_is_bonus(obj: Game, bonus_game_id: int):
    return {
        **obj.__dict__,
        'images': obj.images,
        'is_bonus_game': obj.id == bonus_game_id
    }


@games_router.get('', response_model=List[GameSchemaBasic], tags=['AdminGames'])
async def get(session: Session = Depends(get_db), auth: JwtAuthorizationCredentials = Security(access_security)):
    games = session.scalars(select(Game).where(Game.is_deleted == False).order_by(Game.id.asc()))  # noqa
    if c := session.scalar(select(Config).where(Config.key == 'bonus_game')):
        bonus_game = c.value
    else:
        bonus_game = 9999
    return [game_with_is_bonus(game, int(bonus_game)) for game in games]


@games_router.get('/{game_id}', response_model=GameSchemaWithAttributes, tags=['AdminGames'])
async def get_by_id(game_id: int, session: Session = Depends(get_db),
                    auth: JwtAuthorizationCredentials = Security(access_security)):
    return session.get(Game, game_id)


@games_router.patch('', response_model=UpdateObjectSchema, tags=['AdminGames'])
async def patch(data: GameSchemaUpdate, session: Session = Depends(get_db),
                auth: JwtAuthorizationCredentials = Security(access_security)):
    game = session.get(Game, data.id)

    for k, v in data.model_dump().items():
        if v is not None:
            setattr(game, k, v)

    session.add(game)
    session.commit()
    return {'id': game.id}


@games_router.delete('', response_model=DeletedObjectSchema, tags=['AdminGames'])
async def delete(id: int, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    game = session.get(Game, id)
    game.is_deleted = True
    session.add(game)
    session.commit()
    return {'id': game.id}

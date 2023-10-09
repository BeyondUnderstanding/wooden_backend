from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from db.database import get_db
from models import Game, GameAttribute
from .schema import GameSchema
from ..auth.router import access_security
from ...schema import CreateObjectSchema
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

    return {'created_id': new_game.id}


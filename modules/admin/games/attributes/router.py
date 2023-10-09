from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.database import get_db
from models import GameAttribute
from modules.admin.auth.router import access_security
from modules.admin.games.attributes.schema import GameAttributeWithID
from .schema import GameAttributeCreateSchema
from modules.schema import CreateObjectSchema

attributes_router = APIRouter(prefix='/attribute')


@attributes_router.post('', response_model=CreateObjectSchema, tags=['Attributes'])
async def create_attribute(data: GameAttributeCreateSchema, session: Session = Depends(get_db),
                           auth: JwtAuthorizationCredentials = Security(access_security)):
    new_attribute = GameAttribute(**data.model_dump())  # noqa
    session.add(new_attribute)
    session.commit()
    session.refresh(new_attribute)

    return {'created_id': new_attribute.id}


@attributes_router.get('', response_model=List[GameAttributeWithID])
async def get_attributes(game: int, session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    attributes: List[GameAttribute] = session.scalars(
        select(GameAttribute).where(GameAttribute.game_id == game)
    )
    return attributes


@attributes_router.patch('')
async def update_attribute():
    raise NotImplemented


@attributes_router.delete('')
async def delete_attribute():
    raise NotImplemented

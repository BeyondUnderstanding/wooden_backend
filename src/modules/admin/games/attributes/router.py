from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models import GameAttribute
from src.modules.admin.auth.router import access_security
from src.modules.admin.games.attributes.schema import GameAttributeWithID, GameAttributeOptionalSchema
from .schema import GameAttributeCreateBulkSchema
from src.modules.schema import CreateObjectSchema, UpdateObjectSchema, DeletedObjectSchema, CreateBulkSchema

attributes_router = APIRouter(prefix='/attribute')


@attributes_router.post('', response_model=CreateBulkSchema, tags=['Attributes'])
async def create_attribute(data: GameAttributeCreateBulkSchema, session: Session = Depends(get_db),
                           auth: JwtAuthorizationCredentials = Security(access_security)):
    ids = []
    for att in data.items:
            new_attribute = GameAttribute(**att.model_dump())  # noqa
            session.add(new_attribute)
            session.commit()
            session.refresh(new_attribute)
            ids.append(new_attribute.id)

    return {'ids': ids}


@attributes_router.get('', response_model=List[GameAttributeWithID])
async def get_attributes(game: int, session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    attributes: List[GameAttribute] = session.scalars(select(GameAttribute).where(GameAttribute.game_id == game)) # noqa
    return attributes


@attributes_router.patch('', response_model=UpdateObjectSchema)
async def update_attribute(attribute_id: int, data: GameAttributeOptionalSchema, session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    att = session.get(GameAttribute, attribute_id)
    for k, v in data.model_dump().items():
        if v is not None:
            setattr(att, k, v)
    session.add(att)
    session.commit()
    return {'id': att.id}


@attributes_router.delete('', response_model=DeletedObjectSchema)
async def delete_attribute(attribute_id: int, session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    att = session.get(GameAttribute, attribute_id)
    session.delete(att)
    session.commit()
    return {'id': att.id}

from typing import List

from fastapi import APIRouter, Depends, Security, Query
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.models import GameAttribute
from src.modules.admin.auth.router import access_security
from src.modules.admin.games.attributes.schema import GameAttributeWithID, GameAttributeUpdateBulkSchema
from .schema import GameAttributeCreateBulkSchema
from src.modules.schema import UpdateBulkSchema, DeletedObjectSchema, CreateBulkSchema, DeleteBulkSchema

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


@attributes_router.patch('', response_model=UpdateBulkSchema)
async def update_attribute(data: GameAttributeUpdateBulkSchema, session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    ids = []
    for att in data.items:
        att_model: GameAttribute | None = session.get(GameAttribute, att.id)
        if not att:
            continue
        for k, v in att.model_dump().items():
            if v is not None:
                setattr(att_model, k, v)
        ids.append(att_model)
    session.add_all(ids)
    session.commit()
    session.flush()
    return {'ids': [i.id for i in ids]}


@attributes_router.delete('', response_model=DeleteBulkSchema)
async def delete_attribute(item_id: List[int] = Query(), session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    ids = []
    for att in item_id:
        att = session.get(GameAttribute, att)
        if not att:
            continue
        session.delete(att)
        ids.append(att.id)
    session.commit()
    return {'ids': ids}

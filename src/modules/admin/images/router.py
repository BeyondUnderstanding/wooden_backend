from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from src.models import Image

from src.db.database import get_db
from .schemas import CreateImageSchema, UpdateImageSchema
from ..auth.router import access_security
from ...schema import CreateObjectSchema, UpdateObjectSchema, DeletedObjectSchema

imagerouter = APIRouter(prefix='/image', tags=['Image'])


@imagerouter.post('', response_model=CreateObjectSchema)
async def create(data: CreateImageSchema, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    newimage = Image(**data.model_dump())  # noqa
    session.add(newimage)
    session.commit()
    session.refresh(newimage)

    return {'id': newimage.id}


@imagerouter.patch('', response_model=UpdateObjectSchema)
async def update(data: UpdateImageSchema, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    image = session.get(Image, data.id)

    for k, v in data.model_dump().items():
        if v is not None:
            setattr(image, k, v)

    session.add(image)
    session.commit()
    return {'id': image.id}


@imagerouter.delete('', response_model=DeletedObjectSchema)
async def delete(id: int, session: Session = Depends(get_db),
                 auth: JwtAuthorizationCredentials = Security(access_security)):
    image = session.get(Image, id)
    session.delete(image)
    session.commit()
    return {'id': image.id}


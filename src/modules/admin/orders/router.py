import datetime
from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.db.database import get_db
from src.models import Book, GameToBook, Game
from .grid.router import grid_router
from src.modules.exceptions import NOT_IMPLEMENTED
from .schema import OrderModel, OrderModelFull
from ..auth.router import access_security

orders_router = APIRouter(prefix='/orders')
orders_router.include_router(grid_router)


@orders_router.get('/', tags=['Orders'], response_model=List[OrderModel])
async def get_all(start: int = 0, size: int = 10, payed_only: bool = False, active_only: bool = False,
                  session: Session = Depends(get_db), auth: JwtAuthorizationCredentials = Security(access_security)):
    return session.scalars(select(Book)
                           .distinct(Book.id)
                           .where(
                                and_(
                                    Book.is_payed.in_([True] if payed_only else (True, False)),
                                    datetime.datetime.utcnow() < Book.start_date if active_only else 1==1
                                )
                            )
                           .join(GameToBook)
                           .join(Game).limit(size).offset(start).order_by(Book.id.desc()))


@orders_router.get('/{order_id}', tags=['Orders'], response_model=OrderModelFull)
async def get_one(order_id: int,
                  session: Session = Depends(get_db), auth: JwtAuthorizationCredentials = Security(access_security)):
    return session.get(Book, order_id)


@orders_router.delete('/{order_id}/cancel', tags=['Orders'])
async def cancel_order(order_id: int,
                       session: Session = Depends(get_db),
                       auth: JwtAuthorizationCredentials = Security(access_security)):
    order = session.get(Book, order_id)
    order.is_canceled = True
    if order.is_payed:
        # TODO: Start refund logic
        pass

    # Clear occupied dates for each game in order
    for p in order.games:
        for od in p.occupied_dates:
            session.delete(od)
    session.commit()
    # TODO: Message customer about order cancellation

    return JSONResponse(content={'message': f'Order {order.id} canceled'})


@orders_router.post('/{order_id}/sms', tags=['Orders'])
async def send_message(order_id: int, auth: JwtAuthorizationCredentials = Security(access_security)):
    # TODO: Send customer custom message
    raise NOT_IMPLEMENTED

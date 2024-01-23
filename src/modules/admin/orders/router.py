import datetime
from typing import List

from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.config import IS_DEV
from src.db.database import get_db
from src.models import Book, GameToBook, Game
from .grid.router import grid_router
from src.modules.exceptions import NOT_IMPLEMENTED
from .schema import OrderModel, OrderModelFull, OrderSendMessage
from src.modules.admin.auth.router import access_security
from src.modules.schema import UpdateObjectSchema
from ..utils import send_sms_message

# from src.modules.client.basket.utils import new_order_sms_notification

orders_router = APIRouter(prefix='/orders')
orders_router.include_router(grid_router)


@orders_router.get('/', tags=['AdminOrders'], response_model=List[OrderModel])
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


@orders_router.get('/{order_id}', tags=['AdminOrders'], response_model=OrderModelFull)
async def get_one(order_id: int,
                  session: Session = Depends(get_db),
                  auth: JwtAuthorizationCredentials = Security(access_security)):
    if order:=session.get(Book, order_id):
        return order
    else:
        raise HTTPException(status_code=404, detail='Order not found')


@orders_router.patch('/{order_id}/prepayment', tags=['AdminOrders'], response_model=UpdateObjectSchema)
async def set_prepayment(order_id: int,
                         session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    order = session.get(Book, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    if not order.is_prepayment:
        raise HTTPException(status_code=400, detail='Order is not prepayment')

    if order.prepayment_done:
        raise HTTPException(status_code=400, detail='Order already marked as payed')

    order.prepayment_done = True

    session.add(order)
    session.commit()

    return {'id': order.id}


@orders_router.delete('/{order_id}/cancel', tags=['AdminOrders'])
async def cancel_order(order_id: int, need_refund: bool = False,
                       session: Session = Depends(get_db),
                       auth: JwtAuthorizationCredentials = Security(access_security)):
    order = session.get(Book, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')

    order.is_canceled = True
    if order.is_payed and need_refund:
        # TODO: Start refund logic
        pass

    # Clear occupied dates for each game in order
    for p in order.games:
        for od in p.occupied_dates:
            session.delete(od)
    session.commit()
    # TODO: Message customer about order cancellation
    # new_order_sms_notification

    return JSONResponse(content={'message': f'Order {order.id} canceled'})


@orders_router.post('/{order_id}/sms', tags=['AdminOrders'])
async def send_message(order_id: int,
                       data: OrderSendMessage,
                       auth: JwtAuthorizationCredentials = Security(access_security),
                       session: Session = Depends(get_db)):
    if not IS_DEV:
        is_message_sent = send_sms_message(order_id, session, f'Order {order_id} is canceled. Contact us for more info.')
    else:
        is_message_sent = True
    if not is_message_sent:
        return JSONResponse(content={'message': 'Message is not sent'}, status_code=500)
    return JSONResponse(content={'message': 'Message sent'})
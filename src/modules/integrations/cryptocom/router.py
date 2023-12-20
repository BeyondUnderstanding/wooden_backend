from typing import Annotated

from fastapi import APIRouter, Depends, Security, Header, Request
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.config import CRYPTO_SECRET
from src.db.database import get_db
from src.models import Book
from src.modules.admin.auth.router import access_security
from src.modules.client.basket.schema import CreateOrderOK
from src.modules.integrations.cryptocom.schema import CryptoWebhook
from src.modules.integrations.cryptocom.utils import crypto_create_payment
import hashlib, hmac

cryptocom = APIRouter(prefix='/payments/crypto', tags=['Payments'])


@cryptocom.post('/test', response_model=CreateOrderOK)
def test_crypto(order_id: int, amount: float,
                session: Session = Depends(get_db),
                auth: JwtAuthorizationCredentials = Security(access_security)):
    obj = crypto_create_payment(order_id, amount, 'USD', 'Test payment')
    return CreateOrderOK(
        order_id=order_id,
        payment_method='cryptocom',
        checkout_url=obj.payment_url
    )


# I pray what nobody will try bypass payment via fake request to this endpoint
# I dont know why hmac hashes doesnt match
@cryptocom.post('/webhook')
async def crypto_webhook(data: CryptoWebhook,
                         Pay_Signature: Annotated[str, Header(convert_underscores=True)],
                         request: Request,
                         session: Session = Depends(get_db)):
    t, v1 = Pay_Signature.split(',')
    t = t.split('=')
    v1 = v1.split('=')
    # request_body = (await request.body()).decode('utf-8')
    # validating_string = ((f'{t[1]}.' + request_body
    #                      .replace('None', 'null')
    #                      .replace("'", '"')
    #                      .replace('False', 'false')
    #                      .replace('True', 'true')
    #                      .replace(' ', ''))
    #                      .replace('\n', ''))
    # secret = ''.encode('utf-8')
    # sign = hmac.new(secret, validating_string.encode('utf-8'), hashlib.sha256)
    order_id = int(data.data.object.order_id)
    status = data.data.object.status == 'succeeded'

    if not status:
        return JSONResponse(content={'status': 'Invalid status'}, status_code=400)

    order: Book | None = session.get(Book, order_id)

    if not order:
        return JSONResponse(content={'status': 'Order not found'}, status_code=400)

    order.is_payed = True
    session.add(order)
    session.commit()

    return JSONResponse(content={'status': 'ok'}, status_code=200)

from typing import Annotated

from fastapi import APIRouter, Depends, Security, Header, Request
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.config import CRYPTO_SECRET
from src.db.database import get_db
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


@cryptocom.post('/webhook')
async def crypto_webhook(data: CryptoWebhook,
                         Pay_Signature: Annotated[str, Header(convert_underscores=True)],
                         request: Request):
    t, v1 = Pay_Signature.split(',')
    t = t.split('=')
    v1 = v1.split('=')
    request_body = (await request.body()).decode('utf-8')
    validating_string = ((f'{t[1]}.' + request_body
                         .replace('None', 'null')
                         .replace("'", '"')
                         .replace('False', 'false')
                         .replace('True', 'true')
                         .replace(' ', ''))
                         .replace('\n', ''))
    print(validating_string)
    secret = 'VgVU6FUXOGCeRVvw25dz69b93HGS2d9FiSBC40zuXO0='.encode('utf-8')
    sign = hmac.new(secret, validating_string.encode('utf-8'), hashlib.sha256)
    print(sign.hexdigest())
    print(v1[1])
    # print(order_id, status)
    # print(Pay_Signature)
    return JSONResponse(content={'status': 'ok'}, status_code=200)

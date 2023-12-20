from typing import Annotated

from fastapi import APIRouter, Depends, Security, Header
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.db.database import get_db
from src.modules.admin.auth.router import access_security
from src.modules.client.basket.schema import CreateOrderOK
from src.modules.integrations.cryptocom.schema import CryptoWebhook
from src.modules.integrations.cryptocom.utils import crypto_create_payment

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
def crypto_webhook(data: CryptoWebhook, Pay_Signature: Annotated[str, Header(convert_underscores=True)]):
    order_id = int(data.data.object.order_id)
    status = data.data.object.status == 'succeeded'
    print(order_id, status)
    print(Pay_Signature)
    return JSONResponse(content={'status': 'ok'}, status_code=200)

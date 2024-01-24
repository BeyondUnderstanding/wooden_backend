from typing import Type, Annotated

from fastapi import APIRouter, Depends, Header
from paypalrestsdk.core.environment import SandboxEnvironment, LiveEnvironment
from paypalrestsdk.core.paypal_http_client import PayPalHttpClient
from paypalrestsdk.v1.webhooks import webhook_verify_signature_request
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import PP_ID, PP_SECRET, PP_TEST_ID, PP_TEST_SECRET, IS_DEV
from src.db.database import get_db
from src.models import Book

dev_env = SandboxEnvironment(PP_TEST_ID, PP_TEST_SECRET)
live_env = LiveEnvironment(PP_ID, PP_SECRET)

if IS_DEV:
    client = PayPalHttpClient(environment=dev_env)
else:
    client = PayPalHttpClient(environment=live_env)

paypal = APIRouter(prefix='/payments/paypal')


@paypal.get('/')
async def test_paypal(order_id: int, session: Session = Depends(get_db)):
    from src.modules.integrations.paypal.utils import generate_order
    order: Book | None = session.get(Book, order_id)

    link = generate_order(order)
    return link



@paypal.post('/webhook')
async def webhook(PAYPAL_AUTH_ALGO: Annotated[str, Header(convert_underscores=True)],
                  PAYPAL_CERT_URL: Annotated[str, Header(convert_underscores=True)],
                  PAYPAL_TRANSMISSION_ID: Annotated[str, Header(convert_underscores=True)],
                  PAYPAL_TRANSMISSION_SIG: Annotated[str, Header(convert_underscores=True)],
                  PAYPAL_TRANSMISSION_TIME: Annotated[str, Header(convert_underscores=True)],
                  request: Request,
                  data: dict
                  ):
    WEBHOOK_ID = '9NJ90130N64493809'

    from src.modules.integrations.paypal.utils import validate_webhook
    validate_status = validate_webhook(PAYPAL_AUTH_ALGO,
                     PAYPAL_CERT_URL,
                     PAYPAL_TRANSMISSION_ID,
                     PAYPAL_TRANSMISSION_SIG,
                     PAYPAL_TRANSMISSION_TIME,
                     WEBHOOK_ID,
                     await request.json(),
                     client
                     )
    print(validate_status.verification_status)
    if validate_status.verification_status == 'SUCCESS':
        print('Validate - valid')
    else:
        print('Validate - invalid')
        return JSONResponse(content={'error': 'Invalid request'}, status_code=400)

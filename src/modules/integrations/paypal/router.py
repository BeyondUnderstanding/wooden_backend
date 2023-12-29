from paypalrestsdk.core.environment import SandboxEnvironment
from paypalrestsdk.core.paypal_http_client import PayPalHttpClient
from paypalrestsdk.v1.orders.orders_create_request import OrdersCreateRequest
from src.modules.integrations.paypal.utils import PP_CLIENT_TEST_ID, PP_CLIENT_TEST_SECRET

env = SandboxEnvironment(PP_CLIENT_TEST_ID, PP_CLIENT_TEST_SECRET)
client = PayPalHttpClient(environment=env)

from fastapi import APIRouter

paypal = APIRouter(prefix='/payments/paypal')

@paypal.get('/')
async def test_paypal():
    order = OrdersCreateRequest().request_body({
        'purchase_units': [
            {
                "reference_id": "woodengamesorder_1",
                "description": "WoodenGames Booking",
                "amount": {
                    "currency": "USD",
                    "total": "3"
                },
                "items": [
                    {
                        "name": "Game 1",
                        "sku": "1",
                        "price": "1",
                        "currency": "USD",
                        "quantity": "1"
                    },
                    {
                        "name": "Game 2",
                        "sku": "2",
                        "price": "1",
                        "currency": "USD",
                        "quantity": "1"
                    },
                    {
                        "name": "Game 3",
                        "sku": "3",
                        "price": "1",
                        "currency": "USD",
                        "quantity": "1"
                    }
                ]
            }
        ],
        'redirect_urls': {
            "return_url": "https://woodengames.ge/order/1/success",
            "cancel_url": "https://woodengames.ge/order/1/fail"
        }
    })
    order_response = client.execute(order)
    order_result = order_response.result
    for link in order_result.links:
        print(link.href)
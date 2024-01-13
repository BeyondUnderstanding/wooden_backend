import requests
from paypalrestsdk.v1.orders import OrdersCreateRequest
from requests.auth import HTTPBasicAuth

from src.models import Book

PP_CLIENT_TEST_ID = 'AVcUxSz9mUf9swLQEkQfa8IYqK5ZZ2qEYfCiBje85_5Om8TiniQ3oAt3qd4K1v_UuuXGXpaEFFcJ0M0j'
PP_CLIENT_TEST_SECRET = 'ECRGDFdiKAqbZn8zghyhMHTJMJQo1zzLz8_k--BML8TjUMoPAIMQ3hzJhx7ukmw1nkwSzHnQTszpd98G'


def generate_order(order_id: int,
                   order: Book):
    new_order = OrdersCreateRequest().request_body({
        'purchase_units': [
            {
                "reference_id": f"woodengamesorder_{order_id}",
                "description": "WoodenGames Booking",
                "amount": {
                    "currency": "USD",
                    "total": order.total_price
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

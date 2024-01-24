import json
from math import ceil
from typing import List, OrderedDict

from paypalrestsdk.core import PayPalHttpClient
from paypalrestsdk.v1.orders import OrdersCreateRequest
from paypalrestsdk.v1.webhooks.webhook_verify_signature_request import WebhookVerifySignatureRequest
from src.models import Book, GameToBook
from src.modules.integrations.paypal.router import client


def generate_order(order: Book):
    # TODO: Нужно прикрутить автоматическое получение курса валют
    # 1 GEL = 0.38 USD
    USD_RATE = 0.38

    reference_id = f'woodengames_order_{order.id}'
    amount = round(order.total_price * USD_RATE, 2)
    new_order = OrdersCreateRequest().request_body({
        'purchase_units': [
            {
                "reference_id": reference_id,
                "description": "WoodenGames Booking",
                "amount": {
                    "currency": "USD",
                    "total": amount
                }
            }
        ],
        'redirect_urls': {
            "return_url": f"https://woodengames.ge/order/{order.id}/success",
            "cancel_url": f"https://woodengames.ge/order/{order.id}/fail"
        }
    })
    order_response = client.execute(new_order)
    order_links = order_response.result.links
    return order_links[1].href


def validate_webhook(auth_algo,
                     cert_url,
                     transmission_id,
                     transmission_sig,
                     transmission_time,
                     webhook_id,
                     event: dict,
                     pp_client: PayPalHttpClient):
    ordered_event = json.loads(json.dumps(event), object_pairs_hook=OrderedDict)
    payload = {
        "auth_algo": auth_algo,
        "cert_url": cert_url,
        "transmission_id": transmission_id,
        "transmission_sig": transmission_sig,
        "transmission_time": transmission_time,
        "webhook_id": webhook_id,
        "webhook_event": ordered_event
    }
    print(payload)
    response = pp_client.execute(WebhookVerifySignatureRequest().request_body(payload))
    return response.result
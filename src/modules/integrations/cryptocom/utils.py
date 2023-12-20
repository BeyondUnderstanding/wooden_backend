from requests import post
from src.config import CRYPTO_SECRET
from .schema import CryptoCreatePaymentResponse


def crypto_create_payment(order_id, amount, currency, description):
    request = post('https://pay.crypto.com/api/payments',
                   json={
                       'amount': amount*100*0.37,
                       'currency': currency,
                       'description': description,
                       'order_id': order_id,
                       'return_url': f'https://woodengames.ge/order/{order_id}/complete',
                       'cancel_url': f'https://woodengames.ge/order/{order_id}/failed'
                   },
                   headers={
                       f'Authorization': f'Bearer {CRYPTO_SECRET}'
                   })
    schema = CryptoCreatePaymentResponse.model_validate(request.json())
    return schema

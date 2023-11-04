import hashlib
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from typing import List, Optional
import requests
import json


class BaseAPI:
    def __init__(self):
        self.version = None
        self.urlBase = None
        self.create_order = None
        self.pre_auth_confirm = None
        self.get_saved_card = None


class APIMethodsV1(BaseAPI):
    def __init__(self):
        super().__init__()
        self.version = 1
        self.urlBase = 'https://api.unipay.com/checkout/'
        self.create_order = f'{self.urlBase}/createorder'
        self.pre_auth_confirm = f'{self.urlBase}/confirm'
        self.get_saved_card = f'{self.urlBase}/get-card'


class APIMethodsV2(BaseAPI):
    def __init__(self):
        super().__init__()
        self.version = 2
        self.urlBase = 'http://localhost:8800/custom/checkout/v1'
        self.create_order = f'{self.urlBase}/createorder'
        self.pre_auth_confirm = f'{self.urlBase}/confirm'
        self.get_saved_card = f'{self.urlBase}/get-card'

@dataclass
class OrderItem(DataClassJsonMixin):
    price: float
    quantity: int
    title: str
    description: str


@dataclass
class UniPayResponseData(DataClassJsonMixin):
    Checkout: str
    UnipayOrderHashID: str


@dataclass
class UniPayResponse(DataClassJsonMixin):
    errorcode: int
    message: str
    data: Optional[UniPayResponseData]


class UniPayClient:
    def __init__(self,
                 secretkey: str,
                 merchant_id: int,
                 success_url: str,
                 cancel_url: str,
                 callback_url: str,
                 language: str = 'GE',
                 ):
        self.secretKey = secretkey
        self.successUrl = success_url
        self.cancelUrl = cancel_url
        self.callbackUrl = callback_url
        self.merchant_id = merchant_id
        self.language = language
        self._api = APIMethodsV2()

    def _calculate_hash(self,
                        customer_id,
                        order_id,
                        order_price,
                        order_currency,
                        order_name
                        ) -> str:
        sign_string = \
            f'{self.secretKey}|{self.merchant_id}|{customer_id}|{order_id}|{order_price}|{order_currency}|{order_name}'
        return hashlib.sha256(sign_string.encode('UTF-8')).hexdigest()  # noqa

    def _construct_json(self,
                        hash_str: str,
                        merchant_user: str,
                        merchant_order_id: str,
                        order_price: float,
                        order_currency: str,
                        order_name: str,
                        order_description: str,
                        order_items: List[OrderItem],
                        ):
        items = []
        for item in order_items:
            items.append(item.to_dict())
        return {
            'Hash': hash_str,
            'MerchantID': self.merchant_id,
            'MerchantUser': merchant_user,
            'MerchantOrderID': str(merchant_order_id),
            'OrderPrice': order_price,
            'OrderCurrency': order_currency,
            'SuccessRedirectUrl': self.successUrl,
            'CancelRedirectUrl': self.cancelUrl,
            'CallBackUrl': self.callbackUrl,
            'Language': self.language,
            'OrderName': order_name,
            'OrderDescription': order_description,
            'Items': items
        }

    def _send(self, payload: dict):
        data = requests.post(self._api.create_order, json=payload)
        return UniPayResponse.from_dict(data.json())

    def create_order(self,
                     merchant_order_id: str,
                     merchant_order_user: str,
                     order_price: float,
                     order_name: str,
                     order_description: str = None,
                     items: List[OrderItem] = None,
                     order_currency: str = 'GEL',
                     ) -> UniPayResponse:
        if items is None:
            items = []
        order_hash = self._calculate_hash(merchant_order_user,
                                          merchant_order_id,
                                          order_price,
                                          order_currency,
                                          order_name)
        payload = self._construct_json(hash_str=order_hash,
                                       merchant_user=merchant_order_user,
                                       merchant_order_id=merchant_order_id,
                                       order_price=order_price,
                                       order_currency=order_currency,
                                       order_name=order_name,
                                       order_description=order_description,
                                       order_items=items)
        return self._send(payload)

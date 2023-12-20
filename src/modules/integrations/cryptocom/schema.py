from typing import Optional, Dict

from pydantic import BaseModel


class CryptoCreatePaymentResponse(BaseModel):
    id: str
    amount: float
    currency: str
    description: str
    status: str
    payment_url: str
    return_url: str
    cancel_url: str


class CryptoWebhookDataObject(BaseModel):
    id: str
    amount: int
    amount_refunded: int
    created: int
    crypto_currency: str
    crypto_amount: str
    currency: str
    customer_id: Optional[str | None]
    data_url: str
    payment_url: str
    return_url: str
    cancel_url: str
    description: str
    live_mode: bool
    metadata: Optional[Dict[str, str] | None]
    tax: Optional[Dict[str, str] | None]
    order_id: str
    recipient: str
    status: str
    qr_code: str
    deep_link: str
    expired_at: int
    sub_merchant_id: Optional[str | None]


class CryptoWebhookData(BaseModel):
    object: CryptoWebhookDataObject


class CryptoWebhook(BaseModel):
    id: str
    object_type: str
    type: str
    created: int
    data: CryptoWebhookData

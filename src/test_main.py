import httpx
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


######################
#   User flow tests
######################

from uuid import uuid4
user_uuid = uuid4().hex
user_uuid = f'{user_uuid[0:8]}-{user_uuid[8:12]}-{user_uuid[12:16]}-{user_uuid[16:20]}-{user_uuid[20:]}'


def test_get_products_list():
    resp: httpx.Response = client.get('/v1/client/games', headers={'x-uuid': user_uuid})
    print(resp.json())
    print(user_uuid)
    assert resp.status_code == 200
    assert resp.json()


def test_add_to_basket():
    r1 = client.post('/v1/client/basket', json={'id': 1}, headers={'x-uuid': user_uuid})
    r2 = client.post('/v1/client/basket', json={'id': 2}, headers={'x-uuid': user_uuid})
    r3 = client.post('/v1/client/basket', json={'id': 3}, headers={'x-uuid': user_uuid})
    r3_failed = client.post('/v1/client/basket', json={'id': 3}, headers={'x-uuid': user_uuid})
    assert (r1.status_code == 200 and
            r2.status_code == 200 and
            r3.status_code == 200)
    assert r3_failed.status_code == 400 and r3_failed.json() == {'detail': 'Game already in basket'}


def test_check_basket():
    resp = client.get('/v1/client/basket', headers={'x-uuid': user_uuid})

    assert resp.status_code == 200
    assert len(resp.json()) == 3
from datetime import datetime
from datetime import timedelta

def test_update_basket():
    now = datetime.now() + timedelta(days=128)
    start_date = now.replace(minute=0, second=0, microsecond=0)
    start_date = start_date.isoformat() + '.000Z'

    end_date = now + timedelta(hours=3)
    end_date = end_date.replace(minute=0, second=0, microsecond=0)
    end_date = end_date.isoformat() + '.000Z'

    resp = client.patch('/v1/client/basket', json={
        'start_date': start_date,
        'end_date': end_date
    }, headers={'x-uuid': user_uuid})

    assert resp.status_code == 200
    assert resp.json()['message'] == 'Updated'

def test_delete_items():
    r1 = client.delete('/v1/client/basket', params={'id': 1}, headers={'x-uuid': user_uuid})
    r2 = client.delete('/v1/client/basket', params={'id': 2}, headers={'x-uuid': user_uuid})
    r3 = client.delete('/v1/client/basket', params={'id': 3}, headers={'x-uuid': user_uuid})

    assert (r1.status_code == 200 and
            r2.status_code == 200 and
            r3.status_code == 200)


def test_check_basket_empty():
    resp = client.get('/v1/client/basket', headers={'x-uuid': user_uuid})
    assert len(resp.json()) == 0

def test_create_order():
    client.post('/v1/client/basket', json={'id': 1}, headers={'x-uuid': user_uuid})
    client.post('/v1/client/basket', json={'id': 2}, headers={'x-uuid': user_uuid})
    client.post('/v1/client/basket', json={'id': 3}, headers={'x-uuid': user_uuid})

    resp = client.post('/v1/client/basket/create_order', json={
        'client_name': 'Testing Test',
        'client_phone': '+995718177716',
        'client_email': 'test@example.com',
        'legal_id': '11111111111'
    }, headers={'x-uuid': user_uuid})
    print(resp.json())
    assert resp.status_code == 200
    assert resp.json()['checkout_url']

def test_basket_clearup():
    resp = client.get('/v1/client/basket', headers={'x-uuid': user_uuid})
    assert len(resp.json()) == 0
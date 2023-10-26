from fastapi import APIRouter
from .grid.router import grid_router

orders_router = APIRouter(prefix='/orders')
orders_router.include_router(grid_router)


@orders_router.get('/all', tags=['Orders'])
async def get_all():
    raise NotImplemented


@orders_router.get('/active', tags=['Orders'])
async def get_active():
    raise NotImplemented


@orders_router.get('/info', tags=['Orders'])
async def get_one():
    raise NotImplemented


@orders_router.delete('', tags=['Orders'])
async def cancel_order():
    raise NotImplemented


@orders_router.post('', tags=['Orders'])
async def send_message():
    raise NotImplemented

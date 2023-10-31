from fastapi import APIRouter
from .grid.router import grid_router
from modules.exceptions import NOT_IMPLEMENTED

orders_router = APIRouter(prefix='/orders')
orders_router.include_router(grid_router)


@orders_router.get('/all', tags=['Orders'])
async def get_all():
    raise NOT_IMPLEMENTED


@orders_router.get('/active', tags=['Orders'])
async def get_active():
    raise NOT_IMPLEMENTED


@orders_router.get('/info', tags=['Orders'])
async def get_one():
    raise NOT_IMPLEMENTED


@orders_router.delete('', tags=['Orders'])
async def cancel_order():
    raise NOT_IMPLEMENTED


@orders_router.post('', tags=['Orders'])
async def send_message():
    raise NOT_IMPLEMENTED

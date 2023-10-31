from fastapi import APIRouter

from modules.exceptions import NOT_IMPLEMENTED

grid_router = APIRouter(prefix='/grid')


@grid_router.post('/close', tags=['Grid'])
async def close_timeslot():
    raise NOT_IMPLEMENTED


@grid_router.post('/open', tags=['Grid'])
async def open_timeslot():
    raise NOT_IMPLEMENTED


@grid_router.post('/transfer', tags=['Grid'])
async def transfer_order_to_another_timeslot():
    raise NOT_IMPLEMENTED

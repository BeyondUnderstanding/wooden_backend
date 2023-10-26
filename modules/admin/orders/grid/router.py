from fastapi import APIRouter

grid_router = APIRouter(prefix='/grid')


@grid_router.post('/close', tags=['Grid'])
async def close_timeslot():
    raise NotImplemented


@grid_router.post('/open', tags=['Grid'])
async def open_timeslot():
    raise NotImplemented


@grid_router.post('/transfer', tags=['Grid'])
async def transfer_order_to_another_timeslot():
    raise NotImplemented

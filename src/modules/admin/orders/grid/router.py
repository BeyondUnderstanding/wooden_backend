from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.modules.admin.orders.grid.schema import CloseTimeslotModel
from src.modules.exceptions import NOT_IMPLEMENTED

grid_router = APIRouter(prefix='/grid')


@grid_router.post('/close', tags=['Grid'])
async def close_timeslot(data: CloseTimeslotModel, session: Session = Depends(get_db)):
    raise NOT_IMPLEMENTED


@grid_router.post('/open', tags=['Grid'])
async def open_timeslot(session: Session = Depends(get_db)):
    raise NOT_IMPLEMENTED


@grid_router.post('/transfer', tags=['Grid'])
async def transfer_order_to_another_timeslot(session: Session = Depends(get_db)):
    raise NOT_IMPLEMENTED

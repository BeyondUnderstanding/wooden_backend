from typing import Dict, List

from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from src.modules.client.basket.utils import calculate_delta
from src.modules.admin.auth.router import access_security
from src.db.database import get_db
from src.models import OccupiedDateTime
from src.modules.admin.orders.grid.schema import CloseTimeslotModel, TimeslotSchema, OpenTimeslotModel
from src.modules.exceptions import NOT_IMPLEMENTED

grid_router = APIRouter(prefix='/grid')


@grid_router.get('/', tags=['Grid'], response_model=Dict[str, List[TimeslotSchema]])
async def get_timeslots(session: Session = Depends(get_db),
                        auth: JwtAuthorizationCredentials = Security(access_security)):
    timeslots = session.scalars(select(OccupiedDateTime).order_by(OccupiedDateTime.datetime.asc()))
    dts = {}
    for t in timeslots:
        key = str(t.datetime).split(' ')[0]
        if key in dts.keys():
            dts[key].append(t)
        else:
            dts = dts | {key: [t]}
    # print(dts)
    return dts


@grid_router.post('/close', tags=['Grid'])
async def close_timeslot(data: CloseTimeslotModel, session: Session = Depends(get_db),
                         auth: JwtAuthorizationCredentials = Security(access_security)):
    timeslot = session.scalar(select(OccupiedDateTime).where(OccupiedDateTime.datetime == data.timeslot))
    if timeslot:
        raise HTTPException(status_code=4000, detail={'message': 'Timeslot already exist'})
    if data.all_day:
        start_date = data.timeslot.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = data.timeslot.replace(hour=23, minute=59, second=59, microsecond=0)

        delta = calculate_delta(start_date, end_date)

        occupied_datetimes = session.scalars(
            select(OccupiedDateTime.datetime)
            .where(
                and_(
                    func.extract('hour', OccupiedDateTime.datetime).in_([d.hour for d in delta]),
                    func.extract('day', OccupiedDateTime.datetime) == start_date.day,
                    func.extract('month', OccupiedDateTime.datetime) == start_date.month,
                    func.extract('year', OccupiedDateTime.datetime) == start_date.year,
                )
            )
        )
        if occupied_datetimes.all():
            raise HTTPException(status_code=400, detail={'message': 'Some timeslots already closed',
                                                         'timeslots': [d.strftime('%d/%m/%Y %H:%M:%S') for d in
                                                                       occupied_datetimes]})

        for dt in delta:
            session.add(
                OccupiedDateTime(datetime=dt)
            )
    if not data.all_day:
        session.add(OccupiedDateTime(datetime=data.timeslot.replace(minute=0, second=0, microsecond=0)))
    try:
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail={'message': 'Something goes wrong'})

    return 'ok'


@grid_router.post('/open', tags=['Grid'])
async def open_timeslot(data: OpenTimeslotModel, session: Session = Depends(get_db),
                        auth: JwtAuthorizationCredentials = Security(access_security)):
    ts = session.scalars(select(OccupiedDateTime).where(OccupiedDateTime.datetime == data.timeslot))

    if not ts:
        raise HTTPException(status_code=400, detail={'message': 'Timeslot not found'})

    for t in ts:
        session.delete(t)

    session.commit()

    return 'ok'




@grid_router.post('/transfer', tags=['Grid'])
async def transfer_order_to_another_timeslot(session: Session = Depends(get_db),
                                             auth: JwtAuthorizationCredentials = Security(access_security)):
    raise NOT_IMPLEMENTED

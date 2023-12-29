from pydantic import BaseModel, AwareDatetime, Field, FutureDatetime, NaiveDatetime
from datetime import datetime

from src.modules.admin.games.schema import GameSchemaForAdmin


class CloseTimeslotModel(BaseModel):
    timeslot: NaiveDatetime
    all_day: bool


class OpenTimeslotModel(BaseModel):
    timeslot: NaiveDatetime


class TimeslotSchema(BaseModel):
    game: GameSchemaForAdmin | None
    datetime: datetime

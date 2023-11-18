from pydantic import BaseModel, AwareDatetime, Field


class CloseTimeslotModel(BaseModel):
    timeslot: AwareDatetime
    all_day: bool

    
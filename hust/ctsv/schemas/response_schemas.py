from typing import List

from pydantic import BaseModel
from hust.ctsv.schemas.schemas import ActivityView, Activity, CriteriaType


class Response(BaseModel):
    RespCode: int
    RespText: str


class RspActivityView(Response):
    Activities: List[ActivityView]


class RspActivity(Response):
    UserRole: int
    Activities: List[Activity]


class RspCriteriaTypeDetails(Response):
    CriteriaTypeDetailsLst: List[CriteriaType]

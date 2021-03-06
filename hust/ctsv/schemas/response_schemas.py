from typing import List

from pydantic import BaseModel
from hust.ctsv.schemas.schemas import ActivityView, Activity, CriteriaType


class Response(BaseModel):
    RespCode: int
    RespText: str


class RspActivityView(Response):
    RespCode : int
    RespText : str
    Activities: List[ActivityView]


class RspActivity(Response):
    UserRole: int
    Activities: List[Activity]


class RspCriteriaTypeDetails(Response):
    CriteriaTypeDetailsLst: List[CriteriaType]


class Semester(BaseModel):
    Scode: str
    Student : bool
    Teacher : bool

class SemesterResp(Response):
    SemesterLst : List[Semester]

    def get_current_semester(self):
        if len(self.SemesterLst) != 0:
            return self.SemesterLst[-1].Scode

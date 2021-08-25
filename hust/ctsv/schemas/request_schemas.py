from typing import Optional

import pydantic
from pydantic import BaseModel
from hust.ctsv.schemas.schemas import DRL


class User(BaseModel):
    TokenCode: str
    UserName: str


class RqtActivity(User):
    AId: str


class RqtCriteria(User):
    UserCode: str = None
    Semester: str

    @pydantic.validator('UserCode', pre=True, always=True)
    def default_ts_usercode(cls, v, *, values, **kwargs):
        return v or values['UserName']


class RqtActivityUser(User):
    UserCode: str
    Search: str = ""
    PageNumber: int = 1
    NumberRow: int = 100


class RqtActivityUserCId(RqtActivityUser):
    CId: Optional[int]


class RqtMarkCriteria(User, DRL):
    UserCode: str
    Semester: str
    # CriteriaTypeDetailsLst: List[CriteriaType]

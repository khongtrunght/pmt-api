from typing import Optional, List

from pydantic import BaseModel, validator
import pydantic

class ShowStudent(BaseModel):
    id : str
    ho : Optional[str] = None
    dem  : Optional[str] = None
    ten : Optional[str] = None
    image_url : Optional[str] = None
    fb_link : Optional[str] = None
    fullname : Optional[str] = 'Not Exist'

    @pydantic.validator('fullname', pre=True, always=True)
    def default_ts_usercode(cls, v, *, values, **kwargs):
        try :
            return (" ".join([values['ho'], values['dem'], values['ten']]))
        except:
            return v

    class Config:
        orm_mode = True


class NameStudent(BaseModel):
    id : str
    fullname : Optional[str] = None
    lop_id : Optional[str] = None
    image_url: Optional[str] = None
    fb_link: Optional[str] = None


    class Config:
        orm_mode = True


class ListNameStudent(BaseModel):
    data : List[NameStudent]


class DRLRsp(BaseModel):
    RespCode : Optional[int]
    RespText : Optional[str]
    Mark : int

    @validator("RespCode", pre=True, always=True)
    def set_code(cls, code):
        return code or 0


    @validator("RespText", pre=True, always=True)
    def set_text(cls, text):
        return text or "OK"



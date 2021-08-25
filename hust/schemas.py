from typing import Optional

from pydantic import BaseModel
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
    image_url: Optional[str] = None
    fb_link: Optional[str] = None

    class Config:
        orm_mode = True

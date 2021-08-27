from fastapi import APIRouter

from hust import schemas
from hust.repository import mark
from hust.schemas import DRLRsp

router = APIRouter(prefix="/hust", tags=["Mark Criteria"])


@router.get("/welcome")
def welcome():
    return_string = "Welcome to app, type /hust/?mssv=...&cookies=...?semester=... to cham diem ren luyen"
    return return_string


@router.post("/", response_model=schemas.DRLRsp)
async def mark_criteria(mssv: str, cookies: str, semester: str):
    try :
        drl = mark.mark_criteria(mssv, cookies, semester)
        print(drl)
        return DRLRsp(Mark=drl)
    except:
        return DRLRsp(Mark=0, RespCode=101)

import logging
import time
from typing import Optional

from fastapi import APIRouter

from hust import schemas
from hust.exceptions.exceptions import InvalidTokenException, HetHanDrlException, ChamException
from hust.repository import mark
from hust.schemas import DRLRsp

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/hust", tags=["Mark Criteria"])


@router.get("/welcome")
def welcome():
    return_string = "Welcome to app, type /hust/?mssv=...&cookies=...?semester=... to cham diem ren luyen"
    return return_string


@router.post("/", response_model=schemas.DRLRsp)
async def mark_criteria(mssv: str, cookies: str, semester: Optional[str] = None):
    start = time.time()
    try:
        drl = await mark.mark_criteria(mssv, cookies, semester)
        end = time.time()
        print("Time : " + str(end - start))
        return DRLRsp(Mark=drl)
    except InvalidTokenException as e :
        return DRLRsp(Mark=0, RespCode=e.get_rsp().RespCode, RespText=e.get_rsp().RespText)
    except HetHanDrlException as e :
        print(e)
    except ChamException as e:
        return DRLRsp(Mark=-1, RespCode=e.get_rsp().RespCode, RespText=e.get_rsp().RespText)

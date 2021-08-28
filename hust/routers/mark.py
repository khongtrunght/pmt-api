import logging
import time

from fastapi import APIRouter

from hust import schemas
from hust.repository import mark
from hust.schemas import DRLRsp

logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/hust", tags=["Mark Criteria"])


@router.get("/welcome")
def welcome():
    return_string = "Welcome to app, type /hust/?mssv=...&cookies=...?semester=... to cham diem ren luyen"
    return return_string


@router.post("/", response_model=schemas.DRLRsp)
async def mark_criteria(mssv: str, cookies: str, semester: str):
    start = time.time()
    try:
        drl = await mark.mark_criteria(mssv, cookies, semester)
        end = time.time()
        print("Time : " + str(end - start))
        return DRLRsp(Mark=drl)
    except Exception as e:
        print(e)
        return DRLRsp(Mark=0, RespCode=101)

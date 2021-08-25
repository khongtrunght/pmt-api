from fastapi import APIRouter

from hust.ctsv.main import non_bearer_mark

router = APIRouter(prefix="/hust", tags=["Mark Criteria"])


@router.get("/welcome")
def welcome():
    return_string = "Welcome to app, type /hust/?mssv=...&cookies=...?semester=... to cham diem ren luyen"
    return return_string


@router.get("/")
def mark_criteria(mssv: str, cookies: str, semester: str):
    return non_bearer_mark(mssv, cookies, semester)

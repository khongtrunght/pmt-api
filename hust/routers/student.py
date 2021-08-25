from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from hust.repository import student
from hust import database, schemas
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import parse_obj_as
from typing import List


router = APIRouter(tags=["Student"], prefix="/student")

get_db = database.get_db

templates = Jinja2Templates(directory="resources/frontend")

@router.get("/index/", response_model=schemas.ShowStudent)
def get_student(id: str, db: Session = Depends(get_db)):
    return student.show(id, db)


@router.get("/index_html/", response_class=HTMLResponse)
async def get_html_student(request: Request, id : str, db: Session = Depends(get_db)):
    this_student = student.show(id, db)
    if not this_student.image_url:
        link = student.find_image_url(this_student.id)
        if link:
            this_student.image_url = link
            db.commit()
    show_student = schemas.ShowStudent.from_orm(this_student)
    rq_dict = show_student.dict()
    rq_dict['request'] = request
    return templates.TemplateResponse("result.html", rq_dict)


@router.get("/name/")
async def find_by_name(name : str, db: Session = Depends((get_db))):
    list_student = student.find_by_name(name, db)
    return list_student


@router.get("/name_html/", response_class=HTMLResponse)
def get_html_by_name(request: Request,  name: str, db: Session = Depends(get_db)):
    list_student = student.find_by_name(name, db)
    return templates.TemplateResponse("name.html", {"request": request, "list_student": list_student.data})






import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from hust import models, schemas


def find_image_url(mssv:str):
    url = "https://ctt-sis.hust.edu.vn/Content/Anh/anh_"
    ex_common = ('.jpg', '.png', '.raw', '.jpeg')
    try:
        url_common = [url + mssv + ex for ex in ex_common]
        rs = [requests.get(u).status_code for u in url_common]
        img_url = [r == 200 for r in rs]
    except:
        return None
    if True in img_url:
        right = img_url.index(True)
        return url_common[right]
    else:
        print("sai")
        return None

def show(id: str, db: Session):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        image_url = find_image_url(id)
        if not image_url:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found in sis")
        else:
            return create(schemas.ShowStudent(id=id, image_url=image_url), db)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id {id} not found")
    return student


def create(request: schemas.ShowStudent, db: Session):
    new_student = models.Student(id=request.id, image_url=request.image_url)
    # db.add(new_student)
    # db.commit()
    # db.refresh(new_student)
    return new_student

def find_by_name(name: str, db: Session):
    list_student = db.query(models.Name).filter(models.Name.fullname.contains(name)).limit(10).all()
    if len(list_student) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with name {name} not found")
    for student in list_student:
        print(student)
    return list_student



if __name__ == '__main__':
    print(find_image_url("20194461"))
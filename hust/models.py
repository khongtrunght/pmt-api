from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from hust.database import Base

class Student(Base):
    __tablename__ = 'student'
    id = Column(String, primary_key=True, index=True)
    lop_id = Column(String)
    sdt = Column(String)
    trang_thai = Column(String)
    email = Column(String)
    cmnd = Column(String)
    gioi_tinh = Column(String)
    dob = Column(Date)
    ho = Column(String)
    dem = Column(String)
    ten = Column(String)
    address = Column(String)
    image_url = Column(String)
    fb_link = Column(String)


class Name(Base):
    __tablename__ = 'name'
    id = Column(String, primary_key=True, index=True)
    lop_id = Column(String)
    fullname = Column(String)
    image_url = Column(String)
    fb_link = Column(String)
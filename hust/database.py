from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from hust import models

# SQLALCHEMY_DATABASE_URL = 'postgresql://khongtrunght:@localhost:5432/hust'
SQLALCHEMY_DATABASE_URL =   'postgresql://khpbwsylgrgkrg:53d6c256b753ce00b943acab796daeee2b42ce0730cbe01c2742979e528cbb22@ec2-52-86-2-228.compute-1.amazonaws.com:5432/d355qvebbgd0mr'
# SQLALCHEMY_DATABASE_URL = 'mysql://khongtru_1:Pythonftjava%40123@103.97.125.251:3306/khongtru_hust'

engine = create_engine(SQLALCHEMY_DATABASE_URL) #, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == '__main__':
    db = SessionLocal()
    student = db.query(models.Name).filter(models.Name.fullname== 'Lê Nguyễn Hải Đăng').all()
    if not student:
        print(False)
    print(student[0].id)


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import declarative_base

# Создание объекта FastAPI
app = FastAPI()

# Настройка базы данных MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Zobov:12345@192.168.25.23/isp_p_Zobov"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели SQLAlchemy для пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)  # Указываем длину для VARCHAR
    email = Column(String(100), unique=True, index=True)  # Указываем длину для VARCHAR

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Определение Pydantic модели для пользователя
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для получения пользователя по ID
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Маршрут для создания нового пользователя
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

#
#
#
#
#

# Определение модели SQLAlchemy для пользователя
class Publictaions(Base):
    __tablename__ = "publictaions"

    id = Column(Integer, primary_key=True, index=True)
    views = Column(String(50), index=True)  # Указываем длину для VARCHAR
    name = Column(String(100), unique=True, index=True)  # Указываем длину для VARCHAR
    PRICE = Column(String(100), unique=True, index=True)  # Указываем длину для VARCHAR

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Определение Pydantic модели для пользователя
class PublictaionsCreate(BaseModel):
    views: str
    name: str
    PRICE: str

class PublictaionsResponse(BaseModel):
    id: int
    views: str
    name: str
    PRICE: str

    class Config:
        orm_mode = True

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для получения пользователя по ID
@app.get("/publictaions/{ID}", response_model=PublictaionsResponse)
def read_publictaions(publictaions_ID: int, db: Session = Depends(get_db)):
    publictaions = db.query(Publictaions).filter(Publictaions.ID == publictaions_ID).first()
    if publictaions is None:
        raise HTTPException(status_code=404, detail="Publictaions not found")
    return publictaions

# Маршрут для создания нового пользователя
@app.post("/publictaions", response_model=PublictaionsResponse)
def create_publictaions(publictaions: PublictaionsCreate, db: Session = Depends(get_db)):
    db_publictaions = Publictaions(views=publictaions.views, name=publictaions.name, PRICE=publictaions.PRICE)
    try:
        db.add(db_publictaions)
        db.commit()
        db.refresh(db_publictaions)
        return db_publictaions
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")









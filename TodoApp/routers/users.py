from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Path, Depends
from ..models import Users
from ..database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["users"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECREAT_KEY = 'b8696e33e4dc8062a4ac637d25490b07f87e7d620f1e34a028880d716d62d8d6'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVefification(BaseModel):
    password: str
    new_password: str

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")
    print(user.get("user_id"))
    return db.query(Users).filter(Users.id == user.get("user_id")).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, password_verification: UserVefification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    if not bcrypt_context.verify(password_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")
    user_model.hashed_password = bcrypt_context.hash(password_verification.new_password)
    db.add(user_model)
    db.commit()
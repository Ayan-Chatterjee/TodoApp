from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Path, Depends
from models import Todo
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):

    if user is None or user.get("role").lower() != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")
    return db.query(Todo).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("role").lower() != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed!")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    print(todo_model.title)
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
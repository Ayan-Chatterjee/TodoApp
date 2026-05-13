from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Path, Depends, Request
from ..models import Todo
from ..database import SessionLocal
from .auth import get_current_user
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

# Application pages
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'),db=db)

        if user is None:
            return redirect_to_login()
        todos = db.query(Todo).filter(Todo.owner_id == user.get("user_id")).all()
        return templates.TemplateResponse(name="todo.html", request= request, context={"todos": todos, "user": user})

    except:
        return redirect_to_login()

@router.get('/add-todo-page')
async def render_add_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'),db=db)

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(name="add-todo.html", request=request, context={"user": user})

    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'),db=db)

        if user is None:
            return redirect_to_login()

        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        return templates.TemplateResponse(name="edit-todo.html", request=request, context={"user": user, "todo": todo})

    except:
        return redirect_to_login()

@router.get("/")
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(Todo).filter(Todo.owner_id == user.get("user_id")).all()

@router.get("/todos/{todo_id}", status_code= status.HTTP_200_OK)
async def read_todo(user: user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get("user_id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    todo_model = Todo(**todo_request.model_dump(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0), todo_request: TodoRequest = None):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get("user_id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo_request.model_dump().items():
        setattr(todo_model, key, value)
    db.commit()
    db.refresh(todo_model)
    return todo_model

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get("user_id")).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()


from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
from TodoApp.models import Base
from TodoApp.database import engine
from TodoApp.routers import admin, auth, todos, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette import status

app = FastAPI()

Base.metadata.create_all(bind=engine)
# templates = Jinja2Templates(directory="TodoApp/templates")
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def read_home(request: Request):
    return RedirectResponse(url="/todos/todo-page",status_code= status.HTTP_302_FOUND)

@app.get("/healthy")
def read_healthy():
    return {"status": "healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
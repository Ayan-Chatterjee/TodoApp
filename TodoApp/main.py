from fastapi import FastAPI
from .models import Base
from .database import  engine
from .routers import admin, auth,todos, users


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def read_healthy():
    return {"status": "healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

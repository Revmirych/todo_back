from fastapi import FastAPI
from app.routers import users, tasks, categories

app = FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)

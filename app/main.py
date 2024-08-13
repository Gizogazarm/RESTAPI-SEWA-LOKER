from app import models
from fastapi import FastAPI
from app.database import engine
from app.router import loker,user

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(loker.router)
app.include_router(user.router)
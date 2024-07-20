from app import models
from fastapi import FastAPI
from app.database import engine
from app.router import loker

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(loker.router)
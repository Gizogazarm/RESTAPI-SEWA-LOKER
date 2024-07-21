from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database,schemas
from typing import List
from app.repository import loker


router = APIRouter (
    tags=['loker'],
    prefix="/loker"
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.Loker])
async def get_loker(db: Session = Depends(get_db)):
    return loker.get_loker(db)

@router.post('/',response_model=schemas.LokerOut)
async def create_loker(request: schemas.LokerCreate,db:Session = Depends(get_db)):
    return loker.create_loker(request,db)
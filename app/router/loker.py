from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database,schemas
from typing import List
from ..repository import loker


router = APIRouter (
    tags=['loker'],
    prefix="/loker"
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.Loker])
async def get_loker(db: Session = Depends(get_db)):
    return loker.get_loker(db)

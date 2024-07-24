from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, schemas
from typing import List
from app.repository import loker

router = APIRouter(
    tags=['loker'],
    prefix="/loker"
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.LokerOut])
async def get_loker(db: Session = Depends(get_db)):
    return loker.get_loker(db)

@router.post('/', response_model=schemas.LokerOut)
async def create_loker(request: schemas.LokerBase, db: Session = Depends(get_db)):
    return loker.create_loker(request, db)

@router.get('/{id_loker}')
async def get_id(id_loker:str, db: Session = Depends(get_db)):
    """
    Note :
    - Untuk mengupdate data,  terlebih dahulu untuk mencari Id_Loker
    - Tidak disarankan untuk ditampilkan di interface hanya di program saja

    """
    return loker.get_id_loker(db,id_loker)

@router.put('/update', response_model=schemas.LokerOut)
async def update_loker(id:int, request: schemas.UpdateLoker, db: Session = Depends(get_db)):
    return loker.update_data_by_id(db,id,request)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, schemas
from typing import List
from app.repository import loker

router = APIRouter(
    prefix="/loker"
)

get_db = database.get_db

@router.get('/', response_model=List[schemas.LokerOut], tags=["Loker"])
async def get_loker(db: Session = Depends(get_db)):
    """
    Mendapatkan data loker keseluruhan
    """
    return loker.get_loker(db)

@router.post('/', response_model=schemas.LokerOut, tags=["Loker"])
async def create_loker(request: schemas.LokerBase, db: Session = Depends(get_db)):
    """
    Membuat data loker baru 
    """
    return loker.create_loker(request, db)

@router.get('/{id_loker}',response_model=schemas.Hashing_id, tags=["Hashing Loker"])
async def get_hashing_id(id_loker:str, db: Session = Depends(get_db)):
    """
    Mencari Hashing ID yang sudah dibuat
    """
    return loker.get_id_loker(db,id_loker)

@router.put('/update', response_model=schemas.LokerOut,tags=["Loker"])
async def update_loker(hashing_id: str, request: schemas.UpdateLoker, db: Session = Depends(get_db)):
    """
    Note :
    - Untuk mengupdate data, terlebih dahulu untuk mencari Hashing_id
    - Caranya dengan API Create Hashing (jika sudah ada dengan Get Hashing ID)

    """
    return loker.update_data_by_id(db,hashing_id,request)

@router.post('/{id_loker}', response_model=schemas.Hashing_id,tags=["Hashing Loker"])
async def create_hashing(id_loker: str, db: Session = Depends(get_db)):
    """
    - Buat Create Hashing disini (Jika belum , Kalau sudah maka cari di Get Hashing ID)
    """
    return loker.create_idHashing(db,id_loker)
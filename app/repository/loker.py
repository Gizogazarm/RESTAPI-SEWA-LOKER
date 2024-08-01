from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models as model
from app import schemas
from sqlalchemy.exc import IntegrityError
from app import hashing 



def get_loker(db: Session):
    return db.query(model.Loker).all()

def validate_id(db:Session, request: schemas.LokerBase) -> bool:
    id_query = db.query(model.Loker).filter(model.Loker.id_loker == request.id_loker).first()
    if id_query:
        return True
    else:
        return False

def create_loker(request: schemas.LokerBase, db: Session):
    validate_loker_id = validate_id(db,request)
    if validate_loker_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"ID {request.id_loker} sudah ada"
            )
    else:
        try:
            create_model = model.Loker(**request.model_dump())
            db.add(create_model)
            db.commit()
            db.refresh(create_model)
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Connection to database error")
    return create_model   

def get_id_loker(db:Session, id_loker:str):  
    loker = db.query(model.Loker).filter(model.Loker.id_loker == id_loker).first()

    if not loker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id_loker} tidak ditemukan")
    
    hashing_query = db.query(model.Id_hashing).filter(model.Id_hashing.id_loker == loker.id).first()
    if not hashing_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"hashing ID {id_loker} belum dibuat")
    
    return {"hashing_id" : hashing_query.hashing_id}

def update_data_by_id (db:Session, hashing_id: str, request: schemas.UpdateLoker):
    data = db.query(model.Id_hashing).filter(model.Id_hashing.hashing_id == hashing_id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data yang mau diupdate tidak ditemukan")
     
    id_str = str(data.id_loker)
    status_hash = hashing.verify_hash(id_str,hashing_id)
    if not status_hash:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Hashing tidak ditemukan")

    data_db = db.query(model.Loker).filter(model.Loker.id == data.id_loker).first()

    data_db.nama_loker = request.nama_loker
    data_db.size_loker = request.size_loker
    data_db.harga_sewa = request.harga_sewa

    db.commit()
    db.refresh(data_db)

    return data_db

def validate_id_hashing(db:Session, id: str) -> bool:
    data = db.query(model.Id_hashing).filter(model.Id_hashing.id_loker == id).first()
    if data:
        return True
    else: 
        return False


def create_idHashing(db:Session, id_loker: str):
    data = db.query(model.Loker).filter(model.Loker.id_loker == id_loker).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id_loker} tidak ditemukan")
    
    convert_str = str(data.id)

    validate_id = validate_id_hashing(db,convert_str)
    if validate_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{id_loker} sudah dibuat ")

    create_model = model.Id_hashing(id_loker=convert_str, hashing_id = hashing.get_hash(convert_str))
    db.add(create_model)
    db.commit()
    db.refresh(create_model)
    return create_model



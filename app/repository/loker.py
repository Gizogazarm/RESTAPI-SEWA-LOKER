from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models as model
from app import schemas
from sqlalchemy.exc import IntegrityError



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

def get_id_loker(db:Session, id_loker:str) -> int:
    id_int = db.query(model.Loker).filter(model.Loker.id_loker == id_loker).first()

    if not id_int:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id_loker} tidak ditemukan")
    
    return {"id" : id_int.id}

def update_data_by_id (db:Session, id : int, request: schemas.UpdateLoker):
    data = db.query(model.Loker).filter(model.Loker.id == id).first()

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data yang dicari tidak ada")

    data.nama_loker = request.nama_loker
    data.size_loker = request.size_loker

    db.commit()
    db.refresh(data)

    return data

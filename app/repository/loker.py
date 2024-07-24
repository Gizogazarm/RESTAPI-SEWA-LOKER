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
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"id {request.id_loker} Sudah ada")
        

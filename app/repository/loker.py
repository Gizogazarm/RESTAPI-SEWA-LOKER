from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models as model
from app import schemas
from psycopg2.errors import UniqueViolation
from psycopg2 import errors
from sqlalchemy.exc import IntegrityError as validasi

def get_loker(db: Session):
    return db.query(model.Loker).all()

def create_loker(request: schemas.LokerBase, db: Session):
    
        create_model = model.Loker(
            id_loker=request.id_loker,
            nama_loker=request.nama_loker,
            size_loker=request.size_loker
        )

        try:   
            db.add(create_model)
            db.commit()
            db.refresh(create_model)
        except errors.lookup(UniqueViolation) as e:
            db.rollback()
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"id dengan {request.id_loker} sudah ada"
            )
        except validasi as e:
            db.rollback()
            raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"id dengan {request.id_loker} sudah ada"
            )
    
        return create_model
from sqlalchemy.orm import Session
from app import models as model
from app import schemas

def get_loker(db: Session):
    return db.query(model.Loker).all()

def create_loker(request: schemas.LokerBase, db: Session):
    create_model = model.Loker(
        id_loker=request.id_loker,
        nama_loker=request.nama_loker,
        size_loker=request.size_loker
    )
    db.add(create_model)
    db.commit()
    db.refresh(create_model)
    return create_model

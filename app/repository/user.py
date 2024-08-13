# buat repository user untuk ke router dari schemas yang sudah dibuat
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models as model
from app import schemas
from app import hashing

def input_user(db: Session, request: schemas.InputUser):
    models = model.User(**request.model_dump(exclude={'password'}), 
                             hashing_password=hashing.get_hash(request.password))
    db.add(models)
    db.commit()
    db.refresh(models)

    return schemas.msgCreateUser(
        **request.model_dump(), msg=schemas.MsgCreate.msgSuccess
    )

# coba buat response model untuk create user 
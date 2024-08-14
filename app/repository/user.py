# buat repository user untuk ke router dari schemas yang sudah dibuat
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models as model
from app import schemas
from app import hashing
from pydantic import EmailStr

def input_user(db: Session, request: schemas.InputUser):

    validate_input_user(request.email,request.no_phone,db)

    models = model.User(**request.model_dump(exclude={'password'}), 
                             hashing_password=hashing.get_hash(request.password))
    db.add(models)
    db.commit()
    db.refresh(models)

    return schemas.msgCreateUser(
        **request.model_dump(), msg=schemas.MsgCreate.msgSuccess
    )

def validate_input_user(email:EmailStr,no_phone:str,db:Session):
    email_src = db.query(model.User).filter(model.User.email == email).first()
    no_phone_src = db.query(model.User).filter(model.User.no_phone == no_phone).first()

    if(email_src):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ini sudah terdaftar")
    if(no_phone_src):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Nomer Handphone sudah terdaftar")



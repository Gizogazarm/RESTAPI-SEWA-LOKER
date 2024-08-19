# buat repository user untuk ke router dari schemas yang sudah dibuat
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models as model
from app import schemas
from app import hashing
from pydantic import EmailStr
from app.schemas import NotifMessage as Notification

def input_user(db: Session, request: schemas.InputUser):

    validate_input_user(request.email,request.no_phone,db)

    models = model.User(**request.model_dump(exclude={'password'}), 
                             hashing_password=hashing.get_hash(request.password))
    db.add(models)
    db.commit()
    db.refresh(models)

    return schemas.MsgCreateUser(
        **request.model_dump(), msg=Notification.msgSuccessCreate
    )

# ini akan dihapus dan akan dipindah ke file custom_email.py di branch lain 
def validate_input_user(email:EmailStr,no_phone:str,db:Session):
    email_src = db.query(model.User).filter(model.User.email == email).first()
    no_phone_src = db.query(model.User).filter(model.User.no_phone == no_phone).first()

    if(email_src):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email ini sudah terdaftar")
    if(no_phone_src):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Nomer Handphone sudah terdaftar")


# membuat autehentication user dengan password 
def authentication(db:Session, request: schemas.LoginUser):
    query_src = db.query(model.User).filter(model.User.email == request.email).first()

    if not query_src:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Akun dengan {request.email} tidak ditemukan")
    
    if not hashing.verify_hash(request.password,query_src.hashing_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Password Salah")
    
    return schemas.MsgLoginUser(
        **request.model_dump(), msg=Notification.msgSuccessLogin
    )
# membuat update dengan lupa password sehingga mengupdate hashing yang lama 
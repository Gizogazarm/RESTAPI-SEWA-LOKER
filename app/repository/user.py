# buat repository user untuk ke router dari schemas yang sudah dibuat
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import models as model
from app import schemas
from app import hashing
from pydantic import EmailStr
from app.schemas import NotifMessage as Notification

# Input User
def input_user(db: Session, request: schemas.InputUser):

    validate_input_user(request.email,request.no_phone,db)

    models = model.User(**request.model_dump(exclude={'password'}), 
                             hashing_password=hashing.get_hash(request.password))
    db.add(models)
    db.commit()
    db.refresh(models)

    return schemas.MsgForUser(
        **request.model_dump(), msg=Notification.msgSuccessCreate
    )

# ini akan dihapus dan akan dipindah ke file custom_email.py di branch lain 
def validate_input_user(email:EmailStr,no_phone:str,db:Session):
    email_src = db.query(model.User).filter(model.User.email == email).first()
    no_phone_src = db.query(model.User).filter(model.User.no_phone == no_phone).first()

    if(email_src):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=
                            schemas.MsgForUser(
                                msg=Notification.msgEmailHasBeenRegistered,email=email
                            ).model_dump())
    if(no_phone_src):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=
                            schemas.MsgForUserHp(
                                msg=Notification.msgHandphoneHasBeenRegistered,
                                email=email,
                                no_handphone=no_phone
                            ).model_dump())


# membuat autehentication user dengan password 
def authentication(db:Session, request: schemas.LoginUser):

    email_src = validate_email(db,request.email)
    
    if not hashing.verify_hash(request.password,email_src.hashing_password):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=
                            schemas.MsgForUser(
                                msg=Notification.msgWrongPassword,
                                **request.model_dump()
                            ).model_dump())
    
    return schemas.MsgForUser(
        **request.model_dump(), msg=Notification.msgSuccessLogin
    )

# membuat update password dengan mengganti password yang lama 
def update_password(db: Session, request: schemas.LoginUser):

    email_src = validate_email(db, request.email)
    verify_pasw = hashing.verify_hash(request.password,email_src.hashing_password)

    if verify_pasw:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=schemas.MsgForUser(
            msg=Notification.msgPasswordSame,
            **request.model_dump()
        ).model_dump())
    
    email_src.hashing_password = hashing.get_hash(request.password)
    db.commit()
    db.refresh(email_src)

    return schemas.MsgForUser(
        msg= Notification.msgPasswordChange, **request.model_dump()
    )

def validate_email(db:Session,email: EmailStr):
    email_src = db.query(model.User).filter(model.User.email == email).first()

    if not email_src:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
                            schemas.MsgForUser(
                                msg=Notification.msgEmailNotFound,
                                email=email
                            ).model_dump())
    
    return email_src

"""
1. update schemas error pada user agar bisa menampilkan detail problem yang sama dengan schemas.ModelForUser
   satu konsep , contoh : 
     if verify_pasw:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=schemas.MsgForUser(
            msg=Notification.msgPasswordSame,
            **request.model_dump()
        ).model_dump())  --- > DONE 

2. buat fun untuk kode yang sama seperti verifikasi model agar tidak berulang , contoh : email yang sama --> DONE
3. update fitur untuk lupa password sehingga fitur yang digunakan adalah :
   - hanya input user email saja dan mendapatkan kode untuk input sebagai query nomer kode generator
   - jadi request yang dipakai adalah parent schemas dari login user dan memuat input kode generator untuk wajib
"""
 

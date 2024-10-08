# Membuat kode generator agar dapat memunculkan token dari library secret lalu diubah ke hashlib 
# agar dapat di ubah 
# menggunakan fitur email jika email tidak ditemukan 
# buat database untuk simpan token dengan curent time sehingga ketika expired dapat ditentukan dengan library time
import secrets
import time
from app import hashing as hash
from pydantic import EmailStr
from fastapi import HTTPException, status
from app import schemas
from app.schemas import NotifMessage as Notification

def create_token(email: EmailStr) -> dict:
    token = secrets.token_urlsafe(8)
    start_time = int(time.time())
    hashing_token = hash.get_hash(token)
    return {"email":email,"token":token,"hash_token":hashing_token ,"time": start_time }

def validasi_token(email: EmailStr,token: str, hashing_token: str, start_token:int):
    current_time = int(time.time())
    val_time = current_time - start_token

    if val_time < 900:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=
                            schemas.MsgForUser(
                                msg=Notification.msgTokenExpired, 
                                email=email
                            ))
    
    status_hash = hash.verify_hash(token, hashing_token)

    if not status_hash:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=schemas.MsgForUser(
            msg= Notification.msgWrongToken,
            email=email
        ))



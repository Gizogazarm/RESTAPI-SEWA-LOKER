from pydantic import BaseModel, EmailStr
from fastapi import Form
from enum import Enum
from typing import Annotated

class SizeLoker(str, Enum):
    s = "S"
    m = "M"
    l = "L"
    xl = "XL"
    xxl = "XXL"

class NotifMessage(str,Enum):
    msgSuccessCreate = "Akun Berhasil dibuat"
    msgFailedCreate = "Akun Tidak Berhasil dibuat"
    msgTokenCreate = "Token berhasil dibuat"
    msgSuccessLogin = "Akun Berhasil Login"
    msgFailedLogin = "Akun Tidak Berhasil Login"
    msgPasswordSame = "Mohon ganti password yang baru"
    msgPasswordChange = "Password berhasil diganti"
    msgEmailNotFound = "Email belum terdaftar"
    msgEmailHasBeenRegistered = "Email sudah terdaftar"
    msgHandphoneHasBeenRegistered = "Nomer Handphone sudah terdaftar"
    msgWrongPassword = "Mohon masukan password yang benar"
    msgTokenWasExist = "Token sudah ada , mohon input terlebih dahulu"
    msgWrongToken = "Token yang anda input salah"
    msgTokenExpired = "Masa waktu token sudah habis , mohon buat baru "

class LokerBase(BaseModel):
    id_loker: str
    nama_loker: str
    size_loker: SizeLoker
    harga_sewa: float

class Loker(LokerBase):
    id: int

    class Config:
        orm_mode = True

class LokerOut(LokerBase):
    class Config:
        orm_mode = True

class UpdateLoker(BaseModel):
    nama_loker: str
    size_loker: SizeLoker
    harga_sewa: float

class Hashing_id(BaseModel):
    hashing_id: str

    class Config:
        orm_mode = True

class EmailUser(BaseModel):
    email: Annotated[EmailStr,Form()]

class LoginUser(EmailUser):
    password: Annotated[str,Form()]

class InputUser(LoginUser):
    name: Annotated[str,Form()]
    no_phone: Annotated[str, Form()]
    password: Annotated[str,Form()]
    address: Annotated[str | None , Form()] = None

    class Config:
        orm_mode = True

class MsgForUser(BaseModel):
    msg: NotifMessage
    email:EmailStr
    
class MsgForUserHp(MsgForUser):
    no_handphone: Annotated[str , None] = None

class MsgForCreateToken(MsgForUser):
    token:str
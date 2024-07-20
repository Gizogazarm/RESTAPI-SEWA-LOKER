from pydantic import BaseModel
from enum import Enum

class Size_loker(str,Enum):
    s = "S"
    m = "M"
    l = "L"
    xl = "XL"
    XXL = "XXL"

class Msg(BaseModel):
    Msg: str

class MsgCreateUser(Msg):
    email: str
    reason: str

class Loker(BaseModel):
    id:int
    id_loker: str
    nama_loker: str
    size_loker: Size_loker

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    id: int
    email: str
    name: str
    no_phone: str
    hashing_password: str
    address: str | None = None



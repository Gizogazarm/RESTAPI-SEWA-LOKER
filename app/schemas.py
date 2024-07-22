from pydantic import BaseModel
from enum import Enum

class SizeLoker(str, Enum):
    s = "S"
    m = "M"
    l = "L"
    xl = "XL"
    xxl = "XXL"

class LokerBase(BaseModel):
    id_loker: str
    nama_loker: str
    size_loker: SizeLoker

class Loker(LokerBase):
    id: int

    class Config:
        orm_mode = True

class LokerOut(LokerBase):
    class Config:
        orm_mode = True

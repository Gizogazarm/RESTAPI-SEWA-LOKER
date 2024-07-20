from pydantic import BaseModel
from enum import Enum

class Size_loker(str,Enum):
    s = "S"
    m = "M"
    l = "L"


class Loker(BaseModel):
    id:int
    id_loker: str
    size_loker: Size_loker

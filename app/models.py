from .database import Base
from sqlalchemy import Column, Integer, String, CHAR


class Loker(Base):
    __tablename__="loker"

    id = Column(Integer,autoincrement=True,primary_key=True)
    id_loker = Column(String, unique=True, index=True)
    nama_loker = Column(String)
    size_loker = Column(CHAR(3))


class User(Base):
    __tablename__="user"

    id = Column(Integer, autoincrement=True,primary_key=True)
    email = Column(String, unique=True, index=True)
    no_phone = Column(String, unique=True)
    hashing_password = Column(String)
    
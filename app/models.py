from .database import Base
from sqlalchemy import Column, Integer, String, VARCHAR, Numeric, ForeignKey
from sqlalchemy.orm import relationship


class Loker(Base):
    __tablename__="loker"

    id = Column(Integer,autoincrement=True,primary_key=True)
    id_loker = Column(String, unique=True, index=True)
    nama_loker = Column(String)
    size_loker = Column(VARCHAR(3))
    harga_sewa = Column(Numeric(7,2))

    id_hash = relationship("Id_hashing", back_populates="hash")

class User(Base):
    __tablename__="user_loker"

    id = Column(Integer, autoincrement=True,primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    no_phone = Column(String, unique=True)
    hashing_password = Column(String)
    address = Column(String, default="Indonesia")

class Id_hashing(Base):
    __tablename__="id_hashing"

    no = Column(Integer, primary_key=True, autoincrement=True)
    id_loker = Column(Integer, ForeignKey("loker.id"),unique=True)
    hashing_id = Column(String)

    hash = relationship("Loker", back_populates="id_hash")

   

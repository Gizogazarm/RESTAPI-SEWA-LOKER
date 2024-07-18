from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE = "postgresql://postgres:gizogazarm123@localhost/sewa_loker"

engine = create_engine(SQL_ALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

base = declarative_base()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()


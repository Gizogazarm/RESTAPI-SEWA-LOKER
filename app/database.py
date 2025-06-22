from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE = "postgresql://postgres:gizogazarm123@localhost/sewa_loker"

engine = create_engine(SQL_ALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

# Langkah pertama 
# 1. Buat koneksi database.py ( instance database alchemy ) 
# 2. Buat model database seperti tabel , relasi di models.py
# 3. Buat schema untuk validasi data di schemas.py
# 4. Buat api router di router.py seperti loker.py dan user.py
# 5. Buat repository untuk CRUD di repository seperti loker_function.py dan user_function.py (post , put , delete , update)
# 6. Buat main.py untuk menjalankan aplikasi fastapi
# 7. Buat hashing untuk password di hashing.py
# 8. Buat notifikasi untuk pesan di schemas.py



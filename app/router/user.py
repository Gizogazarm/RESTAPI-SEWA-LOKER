from fastapi import APIRouter,Depends,status
from app import database, schemas
from sqlalchemy.orm import session
from app.repository import user

router = APIRouter (
    prefix="/user"
)

get_db = database.get_db

# Membuat Router untuk create login 
@router.post('/',tags=['User'], status_code=status.HTTP_201_CREATED)
async def input_User(request: schemas.InputUser , db: session = Depends(get_db)):
    """
    Membuat User baru
    """
    return user.input_user(db,request)

@router.post('/login', tags=['User'], status_code=status.HTTP_200_OK)
async def login_User(request: schemas.LoginUser, db:session= Depends(get_db)):
    """
    Authentication Login
    """
    return user.authentication(db,request)

#membuat router untuk update password
@router.put('/update_password',tags=['User'],status_code=status.HTTP_200_OK)
async def change_password(request: schemas.LoginUser, db:session= Depends(get_db)):
    """
    Mengubah pasword setelah login
    """
    return user.update_password(db,request)

# membuat token lupa password
@router.post('/create_token',tags=['Forget Password'],status_code=status.HTTP_201_CREATED)
async def create_token(request: schemas.EmailUser, db:session = Depends(get_db)):
    """
    Mendapatkan Token ketika lupa pasword (Untuk yang pertama kali)
    1. Jika sudah dibuat token dan mendapatkan msg "Token sudah ada , mohon input terlebih dahulu"
    maka harus coba memasukkan token untuk mengkonfirmasi token masih aktif atau tidak 
    2. jika tidak aktif , maka harus update token di method PUT untuk update token
    """
    return user.token_forgetPassword(db,request)
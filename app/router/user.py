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
    return user.input_user(db,request)

@router.post('/login', tags=['User'], status_code=status.HTTP_200_OK)
async def login_User(request: schemas.LoginUser, db:session= Depends(get_db)):
    return user.authentication(db,request)

#membuat router untuk update password
@router.post('/update_password',tags=['User'],status_code=status.HTTP_200_OK)
async def change_password(request: schemas.LoginUser, db:session= Depends(get_db)):
    return user.update_password(db,request)
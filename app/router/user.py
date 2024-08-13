from fastapi import APIRouter,Depends
from app import database, schemas
from sqlalchemy.orm import session
from app.repository import user

router = APIRouter (
    prefix="/user"
)

get_db = database.get_db

# Membuat Router untuk create login 
@router.post('/',tags=['Input User'], response_model=schemas.msgCreateUser)
async def input_User(request: schemas.InputUser , db: session = Depends(get_db)):
    return user.input_user(db,request)
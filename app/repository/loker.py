from sqlalchemy.orm import Session
from .. import models as model

def get_loker(db: Session):
    return db.query(model.Loker).all
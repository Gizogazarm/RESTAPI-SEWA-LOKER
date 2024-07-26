from passlib.context import CryptContext


hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(schema: any):
    return hashing.hash(schema)

def verify_hash(schema, hashed_password):
    return hashing.verify(schema,hashed_password)
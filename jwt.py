from jose import JWTError,jwt
from fastapi import HTTPException, Depends
from passlib.context import  CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from model import User
from sqlalchemy.orm import Session
from db  import get_db
 




SECRET_KEY = "7ff9b67b4b584ab0be8422b0fc5ff279dfc2011ef424655bee89401a9b6f6a04"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password, hashed_password)\


def get_user(db, username:str):
    for i in db :
        if i["username"]==username and i["is_deleted"] == False:
            user_dict = i
            return user_dict 
        
    
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username,User.is_deleted == False).first()
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(data : OAuth2PasswordBearer, expires_delta = None):
    to_encode = data.copy() 
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256") 
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401,detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401,detail="Could not validate credentials")
    return {"username":username}
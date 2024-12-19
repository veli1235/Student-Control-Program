from sqlalchemy.orm import Session
from user_schema import *
from model import User
from fastapi import HTTPException, Depends
from user_exception import *
import  psycopg2 
from setting import DATABASE_URL
import bcrypt
from jwt import get_current_user


def create_user_in_db(data: UserCreateSchema,db:Session):
    hashed_password=bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
    new_user=User(username=data.username,password=hashed_password.decode("utf-8"),role = data.role,is_deleted = False)
    if data.role != "admin" and data.role != "lecturer":
        raise WrongValue
    user=db.query(User).filter(User.username == new_user.username, User.is_deleted == False).first()
    if user:
        raise UserIsExists()
    user1=db.query(User).filter(User.username == new_user.username, User.is_deleted == True).first()
    if user1:
        user1.username = data.username
        user1.password = hashed_password.decode("utf-8")
        user1.role = data.role
        user1.is_deleted = False
        db.commit()
        return {"msg":"new user is created"}
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg":"new user is created"} 

def get_user_from_db(*, db: Session,current_user = Depends(get_current_user)):
    return current_user
    

def delete_user_in_db(*,data:UserDeleteSchema,db:Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    user_in_db = db.query(User).filter(User.username==data.username).first()
    if not user_in_db:
        raise UserNotFound
    if user_in_db.is_deleted == False:
        user_in_db.is_deleted = True
    else : 
        raise UserNotFound
    db.commit()
    return {"msg":"user is deleted"}
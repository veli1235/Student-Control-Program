from fastapi import APIRouter,Depends
from user_service import get_user_from_db, create_user_in_db, delete_user_in_db
from sqlalchemy.orm import Session
from db import get_db
from user_schema import UserCreateSchema, UserDeleteSchema
from jwt import get_current_user

user_router = APIRouter(tags=["This is user router"])


@user_router.get("/user")
def get_user( db : Session=Depends(get_db), current_user = Depends(get_current_user)):
    message = get_user_from_db(db = db, current_user = current_user)
    return message

@user_router.post("/user")
def create_user(item : UserCreateSchema, db:Session = Depends(get_db)):
    message = create_user_in_db(data=item,db=db)
    return message

@user_router.delete("/user")
def delete_user(item: UserDeleteSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    message = delete_user_in_db(data=item,db=db,current_user = current_user)
    return message
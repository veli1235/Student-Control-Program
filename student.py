from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db import get_db
from student_service import get_all_student_from_db,create_student_in_db,delete_student_in_db,get_user_by_id_from_db
from student_schema import StudentCreateSchema,StudentDeleteSchema
from jwt import get_current_user


student_router = APIRouter(tags=["This is student router"])

@student_router.get("/student")
def get_all_student( db : Session=Depends(get_db), current_user = Depends(get_current_user)):
    message = get_all_student_from_db( db = db, current_user = current_user)
    return message


@student_router.get("/student/id")
def get_student_by_id(id : int, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    message = get_user_by_id_from_db(id = id ,db = db, current_user = current_user)
    return message

@student_router.post("/student")
def create_student(item : StudentCreateSchema, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    message = create_student_in_db(data=item,db=db, current_user = current_user)
    return message

@student_router.delete("/student/id")
def delete_student(item : StudentDeleteSchema, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    message = delete_student_in_db(data = item, db = db,current_user = current_user)
    return message
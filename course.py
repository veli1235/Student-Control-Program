from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db import get_db
from course_service import get_all_course_from_db,create_course_in_db,delete_course_in_db,register_course_in_db,get_course_info_from_db
from course_schema import CourseCreateSchema, CourseDeleteSchema, CourseRegisterSchema
from jwt import get_current_user
 

course_router = APIRouter(tags=["This is course router"])

@course_router.get("/all_course")
def get_all_course(db : Session = Depends(get_db),current_user = Depends(get_current_user)):
    message = get_all_course_from_db(db = db, current_user=current_user)
    return message

@course_router.get("/course_info_for_lecturers{course_id}")
def get_course_info(teacher_id : int, db : Session = Depends(get_db)):
    message = get_course_info_from_db(teacher_id = teacher_id , db = db)
    return message

@course_router.post("/course")
def create_course(item : CourseCreateSchema, db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    message = create_course_in_db(data=item,db=db,current_user = current_user)
    return message

@course_router.post("/register")
def register_course(item : CourseRegisterSchema, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    message = register_course_in_db(data=item,db=db,current_user = current_user)
    return message

@course_router.delete("/course_id")
def delete_course(item : CourseDeleteSchema,db : Session = Depends(get_db),current_user =Depends(get_current_user)):
    message = delete_course_in_db(data = item, db = db,current_user = current_user)
    return message
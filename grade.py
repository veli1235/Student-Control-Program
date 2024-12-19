from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db import get_db
from grade_service import get_end_marks_by_course_id, get_end_mark_by_id, \
    calculate_gpa_by_student_id, change_end_mark_by_student_id, add_end_mark_by_student_id,\
          delete_end_mark_by_student_id
from grade_schema import GradeCreateSchema, GradeChangeSchema, GradeDeleteSchema
from jwt import get_current_user

grade_router = APIRouter(tags=["this is grade router"])

@grade_router.get("/grade{student_id}")
def get_end_mark(student_id : int , db : Session = Depends(get_db),current_user = Depends(get_current_user)):
    message = get_end_mark_by_id(student_id = student_id, db = db, current_user=current_user)
    return message

@grade_router.get("/grades/{course_id}")
def get_end_marks(course_id : int, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    message = get_end_marks_by_course_id(course_id = course_id, db = db,current_user = current_user)
    return message

@grade_router.get("/grade/gpa{student_id}")
def calculate_gpa(student_id : int, db : Session = Depends(get_db),current_user = Depends(get_current_user)):
    message = calculate_gpa_by_student_id(student_id = student_id, db = db, current_user=current_user)
    return message

@grade_router.post("/grade{course_id}")
def add_end_mark(student_id :int, item : GradeCreateSchema,db : Session = Depends(get_db), current_user = Depends( get_current_user)):
    message = add_end_mark_by_student_id(data = item, student_id = student_id, db = db,current_user = current_user)
    return message

@grade_router.put("/grade{course_id}")
def change_end_mark(student_id : int, item : GradeChangeSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    message = change_end_mark_by_student_id(data = item, student_id = student_id, db = db, current_user=current_user)
    return message


@grade_router.delete("/grade{course_id}")
def delete_end_mark(student_id : int, item : GradeDeleteSchema, db : Session = Depends(get_db),current_user = Depends(get_current_user)):
    message = delete_end_mark_by_student_id(data = item, student_id = student_id, db = db,current_user = current_user)
    return message
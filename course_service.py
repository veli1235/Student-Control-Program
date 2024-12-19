from sqlalchemy.orm import Session
from course_schema import CourseCreateSchema, CourseDeleteSchema, CourseRegisterSchema
from model import Course,User,Student,StudentCourseRegistration
from fastapi import HTTPException,Depends
import  psycopg2 
from setting import DATABASE_URL
from user_exception import UserNotFound
from jwt import get_current_user


def get_all_course_from_db(db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    courses = db.query(Course).filter(Course.is_deleted == False).all()
    lst = []
    for course in courses:
            if not course.course_name in lst:
                lst.append(course.course_name)
    return lst
        


def get_course_info_from_db(*,teacher_id : int, db : Session):
    course = db.query(Course).filter(Course.teacher_id == teacher_id, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404,detail="course not founded")
    names = db.query(StudentCourseRegistration).filter(
        StudentCourseRegistration.course_name == course.course_name, 
        StudentCourseRegistration.is_deleted == False).all()
    students = db.query(Student).filter()

def create_course_in_db(data: CourseCreateSchema,db:Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    new_course = Course(teacher_id = data.teacher_id, course_name = data.course_name, description = data.description, is_deleted = False)
    course = db.query(Course).filter_by(teacher_id = data.teacher_id,course_name = data.course_name, is_deleted = False).first()
    if course:
        raise HTTPException(status_code=404,detail="this course already created")
    teacher = db.query(User).filter_by(id = data.teacher_id, role = "lecturer", is_deleted = False).first()
    if not teacher:
        raise UserNotFound()
    course1 = db.query(Course).filter_by(teacher_id = data.teacher_id,course_name = data.course_name, is_deleted = True).first()
    if course1:
        course1.is_deleted = False
        course1.teacher_id = data.teacher_id
        course1.course_name = data.course_name
        course1.description = data.description
        db.commit()
        return {"msg":"This course is created"}
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"msg": "this course is created"}

def register_course_in_db(data : CourseRegisterSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    name = db.query(Student).filter(Student.FIN_code == data.FIN_code).first()
    if not name : 
        raise HTTPException(status_code=404,detail="this FIN code have not in db")
    name1 = name.name
    new_student_in_course = StudentCourseRegistration(course_name = data.course_name, name = name1, is_deleted = False)
    student_in_course = db.query(StudentCourseRegistration).filter_by(course_name = new_student_in_course.course_name, name = name1).first()
    if student_in_course : 
       raise HTTPException(status_code=404,detail="this student has already registered in this course")
    courses = db.query(Course).filter(Course.course_name == data.course_name, Course.is_deleted == False).first()
    if  not courses :
        raise HTTPException(status_code=404,detail="course not founded")
    db.add(new_student_in_course)
    db.commit()
    db.refresh(new_student_in_course)
    return{"msg":"student is registered"}

def delete_course_in_db(data : CourseDeleteSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student_in_db1 = db.query(Course).filter(Course.id==data.id,Course.is_deleted == False).first()
    if not student_in_db1:
        raise UserNotFound
    register_in_db = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == student_in_db1.course_name,StudentCourseRegistration.is_deleted == False).all()
    if not register_in_db:
        raise UserWarning
    for student in register_in_db:
        student.is_deleted = True
    student_in_db = db.query(Course).filter(Course.id==data.id,Course.is_deleted == False).update({"is_deleted":True})
    if  not student_in_db :
        raise UserNotFound
    
    db.commit()
    return {"msg":"Course is deleted"}


def delete_course_in_db(data : CourseDeleteSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student_in_db1 = db.query(Course).filter(Course.id==data.id,Course.is_deleted == False).first()
    if not student_in_db1:
        raise UserNotFound
    register_in_db = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == student_in_db1.course_name,StudentCourseRegistration.is_deleted == False).all()
    if not register_in_db:
        raise UserWarning
    for student in register_in_db:
        raise HTTPException(status_code=404, detail="There is a student registered for this course.")
    student_in_db = db.query(Course).filter(Course.id==data.id,Course.is_deleted == False).update({"is_deleted":True})
    if  not student_in_db :
        raise UserNotFound
    
    db.commit()
    return {"msg":"Course is deleted"}
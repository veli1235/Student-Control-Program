from sqlalchemy.orm import Session
from course_schema import CourseCreateSchema, CourseDeleteSchema, CourseRegisterSchema, RegisteredStudentDeleteSchema
from model import Course,User,Student,StudentCourseRegistration
from fastapi import HTTPException,Depends
import  psycopg2 
from setting import DATABASE_URL
from user_exception import UserNotFound
from jwt import get_current_user
from sqlalchemy import desc


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
    course_id = db.query(Course).filter(Course.id != None).order_by(desc(Course.id)).first()
    if course_id is None:
        n = "1"
    else:
        n = str(course_id.id+1)
    new_course = Course(teacher_id = data.teacher_id, course_name = data.course_name+n, description = data.description, is_deleted = False)   
    course_name = ''.join([char for char in new_course.course_name if not char.isdigit()])
    name = db.query(Course).filter(teacher_id = data.teacher_id, course_name = data.course_name, is_deleted = False).first()
    name1 = name.course_name
    course = db.query(Course).filter_by(teacher_id = data.teacher_id,course_name =  name1, is_deleted = False).first()
    if course:
        raise HTTPException(status_code=404,detail="this course already created")
    teacher = db.query(User).filter_by(id = data.teacher_id, role = "lecturer", is_deleted = False).first()
    if not teacher:
        raise UserNotFound()
    course1 = db.query(Course).filter_by(teacher_id = data.teacher_id,course_name = data.course_name+n, is_deleted = True).first()
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
    return {"msg":"this course is created"}

def register_course_in_db(data : CourseRegisterSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    name = db.query(Student).filter(Student.FIN_code == data.FIN_code).first()
    if not name : 
        raise HTTPException(status_code=404,detail="this FIN code have not in db")
    name1 = name.name
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    new_student_in_course = StudentCourseRegistration(course_name = course.course_name, name = name1, is_deleted = False)
    student_in_course = db.query(StudentCourseRegistration).filter_by(course_name = new_student_in_course.course_name, name = name1).first()
    if student_in_course : 
       raise HTTPException(status_code=404,detail="this student has already registered in this course")
    if  not course :
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
    
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    if not course:
            raise HTTPException(status_code=404,detail="course not founded")
    student = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).first()
    if not student:
            course.is_deleted = True
    else:
        raise HTTPException(status_code=404,detail="course can not delete")
    
    db.commit()
    return {"msg":"Course is deleted"}


def deleted_registered_student_from_db(data : RegisteredStudentDeleteSchema,db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student = db.query(Student).filter(Student.id == data.student_id, Student.is_deleted == False).first()
    registered_student = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == data.course_name, StudentCourseRegistration.name== student.name, StudentCourseRegistration.is_deleted == False).first()
    if not registered_student :
        raise HTTPException(status_code=404,detail="student not founded")
    else:
        registered_student.is_deleted = True
        db.commit()
        return {"msg":"this student deleted in student course registration database"}
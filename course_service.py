from sqlalchemy.orm import Session
from course_schema import CourseCreateSchema, CourseDeleteSchema, CourseRegisterSchema, RegisteredStudentDeleteSchema
from model import Course,User,Student,StudentCourseRegistration
from fastapi import HTTPException,Depends
import  psycopg2 
from setting import DATABASE_URL
from user_exception import UserNotFound, WrongRole
from course_exception import *
from student_exception import StudentNotFound
from jwt import get_current_user
from sqlalchemy import desc


def get_all_course_from_db(db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    courses = db.query(Course).filter(Course.is_deleted == False).all()
    lst = []
    for course in courses:
        course_name = ''.join([char for char in course.course_name if  not char.isdigit()])
        if not course_name in lst:
            lst.append(course_name)
    return lst
        


def get_course_info_from_db(*,course_id : int, db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "admin":
            raise WrongRole
    course = db.query(Course).filter(Course.id == course_id, Course.is_deleted == False).first()
    if not course:
        raise CourseNotFound
    registered_student = db.query(StudentCourseRegistration).filter(
        StudentCourseRegistration.course_name == course.course_name,
        StudentCourseRegistration.is_deleted == False
    ).first()
    if not registered_student:
        raise HTTPException(status_code=404,detail="No one has registered for this course")
    surname1 = db.query(Student).filter(Student.name == registered_student.name, Student.is_deleted == False).first()
    
    
    if not surname1:
        raise StudentNotFound

    lst = []
    name = ''.join([char for char in surname1.name if not char.isdigit()])  # `surname1.name` üzərində əməliyyat
    surname = surname1.surname  # `surname1.surname` əldə et
    result = f"student: {name} {surname}"  # nəticə yaradılır
    lst.append(result)

    return {course.course_name: lst}
        

def create_course_in_db(data: CourseCreateSchema, db: Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    
    if current_user["username"] == user.username:
        if user.role == "lecturer":
            raise WrongRole
    
   
    teacher = db.query(User).filter_by(id=data.teacher_id, role="lecturer", is_deleted=False).first()
    if not teacher:
        raise UserNotFound()
    courses = db.query(Course).filter(Course.teacher_id == data.teacher_id).all()
    lst = []
    lst1 = []
    for course in courses:
        name = ''.join([char for char in course.course_name if not char.isdigit()])
        lst.append(name)
        lst1.append(course.course_name)
        if data.course_name in lst:
            a = lst.index(data.course_name)
            b = lst1[a]
            name1 = ''.join([char for char in b if char.isdigit()])
    
            existing_course = db.query(Course).filter(
        Course.teacher_id == data.teacher_id, 
        Course.course_name == data.course_name+name1,  
    ).first()

            if existing_course and existing_course.is_deleted==False:
                raise CourseIsExists  
            elif existing_course and existing_course.is_deleted == True:
                course_id = db.query(Course).filter(Course.id != None).order_by(desc(Course.id)).first()
                if course_id is None:
                    n = "1"
                else:
                    n = str(course_id.id + 1)
                existing_course.teacher_id = data.teacher_id
                existing_course.course_name = data.course_name+name1
                existing_course.is_deleted = False
                db.commit()
                return {"msg":"this course is created"}
    
    course_id = db.query(Course).filter(Course.id != None).order_by(desc(Course.id)).first()
    if course_id is None:
        n = "1"
    else:
        n = str(course_id.id + 1)
    
    new_course = Course(
        teacher_id=data.teacher_id,
        course_name=data.course_name + n,
        description=data.description,
        is_deleted=False
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return {"msg":"This course is created"}
        

def register_course_in_db(data: CourseRegisterSchema, db: Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role == "lecturer":
            raise WrongRole
    student = db.query(Student).filter(Student.FIN_code == data.FIN_code, Student.is_deleted == False).first()
    if not student:
        raise StudentNotFound
    courses = db.query(Course).filter(Course.is_deleted == False).all()
    if not courses:
        raise CourseNotFound
    existing_registration = db.query(StudentCourseRegistration).filter(
        StudentCourseRegistration.course_name == data.course_name,
        StudentCourseRegistration.name == student.name,
        StudentCourseRegistration.is_deleted == False
    ).first()
    if existing_registration:
        raise HTTPException(status_code=404,detail="this registration have in database")
    name = ''.join([char for char in data.course_name if not char.isdigit()])
    course = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.is_deleted == False).first()
    if course:
        for k in  course.course_name:
            name1 = ''.join([char if char != 'İ' else 'I' for char in course.course_name if char.isalpha()])
            print(name)
            print(name1)
            if name == name1:
                raise HTTPException(status_code=404,detail="This registration have in database")
            else:
                new_student_in_course = StudentCourseRegistration(
                course_name=data.course_name,
                name=student.name,  
                is_deleted=False
                )
                db.add(new_student_in_course)
                db.commit()
                db.refresh(new_student_in_course)
                return  {"msg":"this registraron is created"}
    else:
        new_student_in_course = StudentCourseRegistration(
                course_name=data.course_name,
                name=student.name,  
                is_deleted=False
                )
                        
        db.add(new_student_in_course)
        db.commit()
        db.refresh(new_student_in_course)
        return  {"msg":"this registraron is created"}

        
        

def delete_course_in_db(data : CourseDeleteSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    if not course:
            raise CourseNotFound
    student = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).first()
    if not student:
            course.is_deleted = True
    else:
        raise CourseWithActiveRegistrationsException
    
    db.commit()
    return {"msg":"Course is deleted"}


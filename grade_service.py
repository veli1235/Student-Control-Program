from sqlalchemy.orm import Session
from grade_schema import GradeCreateSchema, GradeChangeSchema, GradeDeleteSchema
from model import User,Student,Course,StudentCourseRegistration
from fastapi import HTTPException,Depends
import  psycopg2 
from setting import DATABASE_URL 
from jwt import get_current_user
from user_exception import WrongRole,WrongValue
from student_exception import StudentNotFound
from course_exception import CourseNotFound
from grade_exception import EndMarkNotFounded, StudentNotRegisteredInCourse, AddedEndMark


def get_end_mark_by_id(*,student_id : int, db :Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if not student:
        raise StudentNotFound
    register_course = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.is_deleted == False).all()
    if    not register_course:
        raise StudentNotFound
    result = {i.course_name : i.end_mark for i in register_course}
    return result


def get_end_marks_by_course_id(*,course_id : int,db: Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    lst = []
    course = db.query(Course).filter(Course.id == course_id, Course.is_deleted == False).first()
    if not course:
        raise CourseNotFound
    end_marks = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).all()
    for i in end_marks:
        if i.end_mark is not None:
            name = ''.join([char for char in i.name if not char.isdigit()]) 
            mark = i.end_mark
            result = f"{name}: {mark}"  
            lst.append(result)
    if len(lst) == 0 :
        raise EndMarkNotFounded
    return lst
    


def calculate_gpa_by_student_id(*,student_id : int, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if not student :
        raise StudentNotFound
    name = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name,StudentCourseRegistration.is_deleted == False).all()
    lst = []
    lst1 = []
    for i in name : 
            name = ''.join([char for char in i.name if not char.isdigit()])
            lst.append(name)
            if i.end_mark == "A":
                mark = 4
                lst1.append(mark)
            elif i.end_mark == "B":
                mark = 3
                lst1.append(mark)
            elif i.end_mark == "C":
                mark = 2
                lst1.append(mark)
            elif i.end_mark == "D":
                mark = 1
                lst1.append(mark)
            else: 
                mark = 0
                lst1.append(mark)
    n = len(lst)
    calculate_gpa = sum(lst1)/n
    return {name : calculate_gpa}

def add_end_mark_by_student_id(*,student_id:int,data : GradeCreateSchema, db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if course and not student:
        raise StudentNotFound
    elif not course and student:
        raise CourseNotFound
    elif course and student:
        register_student = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).first()
        if not register_student : 
            raise StudentNotRegisteredInCourse
        if register_student.end_mark is  None:
            if data.end_mark == "A" or data.end_mark == "B" or data.end_mark == "C" or data.end_mark == "D" or data.end_mark == "F" :
                register_student.end_mark = data.end_mark
                db.commit()
                return {"msg":"end mark added"}
            else:
                raise WrongValue
        else:
            raise AddedEndMark
    else:
        raise StudentNotFound and CourseNotFound
        
def change_end_mark_by_student_id(*,student_id : int, data : GradeChangeSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if course and student:
        register_student = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).first()
        if register_student.end_mark is not None:
            if data.end_mark == "A" or data.end_mark == "B" or data.end_mark == "C" or data.end_mark == "D" or data.end_mark == "F" :
                register_student.end_mark = data.end_mark
            db.commit()
            return {"msg":"end mark changed"}
        else : 
            raise EndMarkNotFounded

def delete_end_mark_by_student_id(*,student_id : int, data : GradeDeleteSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise WrongRole
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if course and not student:
        raise StudentNotFound
    elif not course and student:
        raise CourseNotFound
    elif course and student:
        register_student = db.query(StudentCourseRegistration).filter(
        StudentCourseRegistration.name == student.name,
        StudentCourseRegistration.course_name == course.course_name,
        StudentCourseRegistration.is_deleted == False).first()
        if register_student.end_mark is not None:
            register_student.end_mark = None
            db.commit()
            return {"msg":"end mark deleted"}
    else : 
        raise EndMarkNotFounded
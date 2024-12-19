from sqlalchemy.orm import Session
from grade_schema import GradeCreateSchema, GradeChangeSchema, GradeDeleteSchema
from model import User,Student,Course,StudentCourseRegistration
from fastapi import HTTPException,Depends
import  psycopg2 
from setting import DATABASE_URL 
from jwt import get_current_user


def get_end_mark_by_id(*,student_id : int, db :Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if not student:
        raise HTTPException(status_code=404,detail="student not founded")
    register_course = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.is_deleted == False).all()
    if    not register_course:
        raise HTTPException(status_code=404,detail="Student not founded")
    result = {i.course_name : i.end_mark for i in register_course}
    return result


def get_end_marks_by_course_id(*,course_id : int,db: Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    lst = []
    course = db.query(Course).filter(Course.id == course_id, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404,detail="course not founded")
    end_marks = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).all()
    for i in end_marks:
        if i.end_mark is not None:
            name = ''.join([char for char in i.name if not char.isdigit()]) 
            mark = i.end_mark
            result = f"{name}: {mark}"  
            lst.append(result)
    if len(lst) == 0 :
        raise HTTPException(status_code=404, detail="end mark not founded")
    return lst
    


def calculate_gpa_by_student_id(*,student_id : int, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if not student :
        raise HTTPException(status_code=404,detail="student not founded")
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
            raise HTTPException(status_code=401,detail="This function is only for admins")
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if course and not student:
        raise HTTPException(status_code=404,detail="student not founded")
    elif not course and student:
        raise HTTPException(status_code=404, detail="course not founded")
    elif course and student:
        register_student = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.course_name == course.course_name, StudentCourseRegistration.is_deleted == False).first()
        if not register_student : 
            raise HTTPException(status_code=404,detail="The user  has not registered for this course.")
        if register_student.end_mark is  None:
            if data.end_mark == "A" or data.end_mark == "B" or data.end_mark == "C" or data.end_mark == "D" or data.end_mark == "F" :
                register_student.end_mark = data.end_mark
                db.commit()
                return {"msg":"end mark added"}
        else:
            raise HTTPException(status_code=401,detail="End mark  has been entered for this student.")
    else:
        raise HTTPException(status_code=404, detail="user and course not founded")
        
def change_end_mark_by_student_id(*,student_id : int, data : GradeChangeSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
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
            raise HTTPException(status_code=404,detail="No mark has been added for this student")

def delete_end_mark_by_student_id(*,student_id : int, data : GradeDeleteSchema, db : Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    course = db.query(Course).filter(Course.id == data.course_id, Course.is_deleted == False).first()
    student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == False).first()
    if course and not student:
        raise HTTPException(status_code=404,detail="student not founded")
    elif not course and student:
        raise HTTPException(status_code=404, detail="course not founded")
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
        raise HTTPException(status_code=404,detail="No mark has been added for this student")


from sqlalchemy.orm import Session
from sqlalchemy import desc
from student_schema import StudentCreateSchema, StudentDeleteSchema
from model import User,Student,Course,StudentCourseRegistration
from fastapi import HTTPException,Depends
from student_exception import *
import  psycopg2 
from setting import DATABASE_URL 
from jwt import get_current_user


def get_all_student_from_db(*,db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    lst = []
    student = db.query(Student).filter(Student.is_deleted == False).all()
    for i in student:
        name = ''.join([char for char in i.name if not char.isdigit()])
        surname = i.surname
        result = f"student : {name} {surname}"
        lst.append(result)
    return lst

def get_user_by_id_from_db(*,id : int,db : Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student = db.query(Student).filter(Student.id == id, Student.is_deleted == False).first()
    if not student:
        raise StudentNotFound()
    
    register_course = db.query(StudentCourseRegistration).filter(StudentCourseRegistration.name == student.name, StudentCourseRegistration.is_deleted == False).all()
    if not register_course:
        result1 = "null"
        a = student.name
        for i in student.name:
            if i.isdigit():
                b = a.replace(i, "")
        return {"name":b,"surname":student.surname,"birthdate":student.birthdate,"course_name":result1}
        
    else:
        result = ", ".join(i.course_name for i in register_course)
        a = student.name
        for i in register_course:
            name = ''.join([char for char in i.name if not char.isdigit()])
        return {"name":name,"surname":student.surname,"birthdate":student.birthdate,"course_name":result}



def create_student_in_db(data: StudentCreateSchema,db:Session,current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student_id = db.query(Student).filter(Student.id != None ).order_by(desc(Student.id)).first()
    if student_id is None:
        n = "1"
    else:
        n = str(student_id.id+1)
    new_student = Student(name = data.name+n, surname = data.surname, FIN_code = data.FINcode, birthdate = data.birthdate, is_deleted = False)
    student = db.query(Student).filter(Student.FIN_code == new_student.FIN_code, Student.is_deleted == False).first()
    if student:
        raise StudentIsExists()
    student1 = db.query(Student).filter(Student.FIN_code == new_student.FIN_code, Student.is_deleted == True).first()
    name = db.query(Student).filter(new_student.name == Student.name).order_by(desc(Student.id)).first()
    if student1:
        n = str(student1.id)
        student1.is_deleted = False
        student1.name = data.name+n
        student1.surname = data.surname
        student1.birthdate = data.birthdate
        db.commit()
        return {"msg":"new student is created"}
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"msg":"new student is created"}

def delete_student_in_db(*,data:StudentDeleteSchema,db:Session, current_user = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user["username"], User.is_deleted == False).first()
    if current_user["username"] == user.username:
        if user.role  == "lecturer":
            raise HTTPException(status_code=401,detail="This function is only for admins")
    student_in_db = db.query(Student).filter(Student.id==data.id, Student.is_deleted == False).update({"is_deleted":True})
    if  not student_in_db :
        raise StudentNotFound
    db.commit()
    return {"msg":"student is deleted"}
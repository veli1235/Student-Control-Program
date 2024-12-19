from sqlalchemy import Column,Integer,String,Date,Boolean
from db import Base,engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    role = Column(String)
    is_deleted = Column(Boolean)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    surname = Column(String)
    FIN_code = Column(String,unique=True)
    birthdate = Column(Date)
    is_deleted = Column(Boolean)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer,primary_key=True)
    teacher_id = Column(Integer)
    course_name = Column(String)
    description = Column(String)
    is_deleted = Column(Boolean)


class StudentCourseRegistration(Base):
    __tablename__ = "student_course_registrations"
    id = Column(Integer,primary_key=True)
    course_name = Column(String)
    name = Column(String)
    end_mark = Column(String)
    is_deleted = Column(Boolean)

Base.metadata.create_all(bind=engine)
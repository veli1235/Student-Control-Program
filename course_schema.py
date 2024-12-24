
from pydantic import BaseModel


class CourseCreateSchema(BaseModel):
    teacher_id : int
    course_name : str
    description : str
    class Config:
        extra = "forbid"


class CourseDeleteSchema(BaseModel):
    course_id : int
    class Config:
        extra = "forbid"

class CourseRegisterSchema(BaseModel):
    course_id : int
    course_name : str
    FIN_code : str
    class Config:
        extra = "forbid"

class RegisteredStudentDeleteSchema(BaseModel):
    course_name : str
    student_id: int
    class Config:
        extra = "forbid"

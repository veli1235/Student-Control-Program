from pydantic import BaseModel


class CourseCreateSchema(BaseModel):
    teacher_id : int
    course_name : str
    description : str
    class Config:
        extra = "forbid"


class CourseDeleteSchema(BaseModel):
    id : int
    class Config:
        extra = "forbid"

class CourseRegisterSchema(BaseModel):
    course_name : str
    FIN_code : str
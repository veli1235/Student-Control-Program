from pydantic import BaseModel
from datetime import date

class GradeCreateSchema(BaseModel):
    course_id : int
    end_mark : str
    class Config:
        extra = "forbid"

class GradeChangeSchema(BaseModel):
    course_id : int
    end_mark : str
    class Config:
        extra = "forbid"

class GradeDeleteSchema(BaseModel):
    course_id : int
    class Config:
        extra = "forbid"
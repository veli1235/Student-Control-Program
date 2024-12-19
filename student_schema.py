from pydantic import BaseModel
from datetime import date

class StudentCreateSchema(BaseModel):
    name : str 
    surname : str
    FINcode : str
    birthdate : date
    class Config:
        extra = "forbid"

class StudentDeleteSchema(BaseModel):
    id : int
    class Config:
        extra = "forbid"
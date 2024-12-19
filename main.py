from fastapi import FastAPI,Depends
from db import get_db
from sqlalchemy.orm import Session
from user import user_router
from student import student_router
from course import course_router
from grade import grade_router
from login import login_router

app = FastAPI(title="My Project",version="0.1.0")

@app.get("/")
def health_check():
    return {"msg":"salam"}

app.include_router(login_router)
app.include_router(user_router)
app.include_router(student_router)
app.include_router(course_router)
app.include_router(grade_router)

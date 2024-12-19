from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    username : str
    password : str
    role : str 
    class Config:
        extra = "forbid"

class UserDeleteSchema(BaseModel):
    username: str
    class Config:
        extra = "forbid"
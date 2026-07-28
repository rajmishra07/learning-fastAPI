from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class showBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True   

class User(BaseModel):
    name: str
    email: str
    password: str         
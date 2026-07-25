from fastapi import FastAPI
from pydantic import BaseModel 
from typing import Optional
app = FastAPI()

@app.get("/blog")
def index(limit: int =10 , published: bool = True, sort: Optional[str] = None):     
    if published:
        return {"data": f"Published blog list with limit {limit}" }
    else:
        return {"data": f"Unpublished blog list with limit {limit}" }

@app.get("/blog/{blog_id}")
def show(blog_id: int):
    return {"data": blog_id}    


@app.get("/blog/{blog_id}/comments")
def comments(blog_id: int):
    return {"data": {"1", "2"}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    return {"data":f"Blog is created with title as {request.title} and body as {request.body} and published status is {request.published}"}
  
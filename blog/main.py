from fastapi import FastAPI,Depends,Response,status ,HTTPException
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

# Create all database tables if they don't already exist
models.Base.metadata.create_all(bind=engine)         

@app.post("/blog", status_code=201,tags=["Blogs"])
def create(request: schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code = status.HTTP_204_NO_CONTENT,tags=["Blogs"])
def destroy(id:int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} is not available")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED,tags=["Blogs"])
def update(id:int,request : schemas.Blog, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} is not available")
    blog.update(request.model_dump(),synchronize_session=False)
    db.commit()
    return "updated"


@app.get("/blog", response_model = list[schemas.showBlog],tags=["Blogs"])
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 

@app.get("/blog/{id}",response_model = schemas.showBlog,tags=["Blogs"])
def show(id: int ,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Blog with id {id} is not available")
    return blog


@app.post('/user', status_code=status.HTTP_201_CREATED,response_model=schemas.showUser,tags=["Users"])
def create_user(request: schemas.User , db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)  
    db.commit()
    db.refresh(new_user)          
    return new_user

@app.get('/user/{id}',response_model=schemas.showUser,tags=["Users"])
def show_user(id: int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id {id} is not available")
    return user
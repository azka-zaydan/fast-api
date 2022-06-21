from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends
from app import apimodels
from app.apimodels import Base
from app.apidatabase import engine, get_db_conn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles as sf
from fastapi.requests import Request
from app.schemas import CreatePost, Post, UpdatePost, UserCreate, UserOut
from typing import List
from app.utils import hashpass

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", sf(directory="app/static"), name="static")
app.mount('/scripts', sf(directory='app/scripts'),name='scripts')
templates = Jinja2Templates(directory='app/templates')

#  API starts here

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request':request,'title': 'Home'})


@app.get('/posts',response_model=List[Post])
async def all_posts(db: Session = Depends(get_db_conn)):
    dbq = db.query(apimodels.Post)
    posts = dbq.all()
    return posts


@app.get('/posts/{search_id}',response_model=Post)
async def get_post_with_id(search_id: int, db: Session = Depends(get_db_conn)):
    result = db.query(apimodels.Post).filter(apimodels.Post.id == search_id).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {search_id}, does not exist")
    else:
        return result


# want title, and content both string
@app.post('/posts', status_code=status.HTTP_201_CREATED,response_model=Post)
async def post(post: CreatePost, db: Session = Depends(get_db_conn)):
    result = apimodels.Post(**post.dict())
    db.add(result)
    db.commit()
    db.refresh(result)

    return result


@app.delete('/posts/{search_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_post(search_id: int, db: Session = Depends(get_db_conn)):
    result = db.query(apimodels.Post).filter(apimodels.Post.id == search_id)
    if result.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {search_id}, does not exist")
    else:
        result.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{search_id}',response_model=Post)
def update_post(search_id: int, post: UpdatePost, db: Session = Depends(get_db_conn)):
    query = db.query(apimodels.Post).filter(apimodels.Post.id == search_id)
    result = query.first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {search_id}, does not exist")
    else:
        query.update(post.dict(), synchronize_session=False)
        db.commit()
        return query.first()

@app.post('/users',status_code=status.HTTP_201_CREATED,response_model=UserOut)
def create_user(user:UserCreate,db: Session = Depends(get_db_conn)):
    hash_password = hashpass(user.password)
    user.password = hash_password
    result = apimodels.User(**user.dict())
    db.add(result)
    db.commit()
    db.refresh(result)
    
    return result
    


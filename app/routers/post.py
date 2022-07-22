from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models
from app.database import get_db_conn
from app.oauth2 import get_current_user
from app.schemas import CreatePost, Post, UpdatePost


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#  API starts here


@router.get('/', response_model=List[Post])
async def all_posts(db: Session = Depends(get_db_conn), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    ''' ayam '''
    dbq = db.query(models.Post)
    posts = dbq.filter(models.Post.owner_id ==
                       current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/{search_id}', response_model=Post)
async def get_post_with_id(search_id: int, db: Session = Depends(get_db_conn)):
    result_post = db.query(models.Post).filter(
        models.Post.id == search_id).first()
    if result_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {search_id}, does not exist")
    else:
        return result_post


# want title, and content both string
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
async def result(post_create: CreatePost, db: Session = Depends(get_db_conn), current_user: int = Depends(get_current_user)):
    # print(current_user)
    dict_post = post_create.dict()
    dict_post['owner_id'] = current_user.id
    result_post = models.Post(**dict_post)
    db.add(result_post)
    db.commit()
    db.refresh(result_post)

    return result_post


@router.delete('/{search_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_post(search_id: int, db: Session = Depends(get_db_conn), _current_user: int = Depends(get_current_user)):
    result_post = db.query(models.Post).filter(models.Post.id == search_id)
    if result_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {search_id}, does not exist")

    if result_post.first().owner_id == _current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    result_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{search_id}', response_model=Post)
async def update_post(search_id: int, post_update: UpdatePost, db: Session = Depends(get_db_conn), _current_user: int = Depends(get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == search_id)
    post = query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {search_id}, does not exist")
    if post.owner_id == _current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action')

    query.update(post_update.dict(), synchronize_session=False)
    db.commit()
    return query.first()

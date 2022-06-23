from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import apimodels
from app.apidatabase import get_db_conn
from app.schemas import CreatePost, Post, UpdatePost
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#  API starts here


@router.get('/',response_model=List[Post])
async def all_posts(db: Session = Depends(get_db_conn)):
    dbq = db.query(apimodels.Post)
    posts = dbq.all()
    return posts


@router.get('/{search_id}',response_model=Post)
async def get_post_with_id(search_id: int, db: Session = Depends(get_db_conn)):
    result = db.query(apimodels.Post).filter(apimodels.Post.id == search_id).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {search_id}, does not exist")
    else:
        return result


# want title, and content both string
@router.post('/', status_code=status.HTTP_201_CREATED,response_model=Post)
async def post(post: CreatePost, db: Session = Depends(get_db_conn)):
    result = apimodels.Post(**post.dict())
    db.add(result)
    db.commit()
    db.refresh(result)

    return result


@router.delete('/{search_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_post(search_id: int, db: Session = Depends(get_db_conn)):
    result = db.query(apimodels.Post).filter(apimodels.Post.id == search_id)
    if result.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {search_id}, does not exist")
    else:
        result.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{search_id}',response_model=Post)
async def update_post(search_id: int, post: UpdatePost, db: Session = Depends(get_db_conn)):
    query = db.query(apimodels.Post).filter(apimodels.Post.id == search_id)
    result = query.first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {search_id}, does not exist")
    else:
        query.update(post.dict(), synchronize_session=False)
        db.commit()
        return query.first()
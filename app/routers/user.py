from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from app import apimodels
from app.apidatabase import get_db_conn
from app.schemas import UserCreate, UserOut
from app.utils import hashpass

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UserOut)
async def create_user(user:UserCreate,db: Session = Depends(get_db_conn)):
    hash_password = hashpass(user.password)
    user.password = hash_password
    result = apimodels.User(**user.dict())
    db.add(result)
    db.commit()
    db.refresh(result)
    
    return result

@router.get('/{search_id}',response_model=UserOut)
async def get_user(search_id: int, db: Session = Depends(get_db_conn)):
    user = db.query(apimodels.User).filter(apimodels.User.id == search_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {search_id}, does not exist")
    
    return user
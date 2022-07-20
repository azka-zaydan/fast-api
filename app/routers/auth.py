from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import app.models as models
from app.schemas import Token
from app.oauth2 import create_access_token
from app.database import get_db_conn
from app.util.utils import verify

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_conn)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    access_token = create_access_token(data={"user_id": user.id})

    # create a token
    return {
        "access_token": access_token, "token_type": "bearer"
    }

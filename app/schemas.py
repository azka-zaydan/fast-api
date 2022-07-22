from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    title: str
    content: str
    published: bool = True


class UpdatePost(PostBase):
    title: str
    content: str
    published: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin (BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserPost(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserPost

    class Config:
        orm_mode = True

import imp
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    title: str
    content: str
    publised: bool = True

class UpdatePost(PostBase):
    title: str
    content: str
    published: bool
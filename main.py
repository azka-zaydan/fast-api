import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str  # we can use this instead of key value dictionaries
    content: str
    published: bool = True
    rating: Optional[int] = 0


@app.get('/')
async def root():
    return "this is the home"


@app.get('/posts')
async def all_posts():
    return {"posts": "this is all the posts"}


@app.post('/')
async def root_post():
    return "this is also home, but with post method"


@app.get('/posts/{search_id}')
async def get_post_with_id(search_id: int):
    return {"this is your post id": search_id}


# want title, and content both string
@app.post('/posts')
async def post(post: Post):
    to_dict = post.dict()
    return {"this is your payload": {
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "rating": post.rating
    }}


if __name__ == "__main__":
    os.system("uvicorn main:app --reload")

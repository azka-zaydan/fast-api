import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

def get_db_conn():

    data = {
        "host": "localhost",
        "port": "6033",
        "user": "root",
        "password": "1234",
        "database": "fastdb"
    }
    try:
        db_conn = mysql.connector.connect(**data)
        return db_conn
    except:
        print("Error")

class Post(BaseModel):
    title: str  # we can use this instead of key value dictionaries
    content: str
    published: bool = True # set a default value
    rating: Optional[int] = 0 # make it optional


@app.get('/')
async def root():
    return "this is the home"


@app.get('/posts')
async def all_posts():
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("select * from posts")
    result = cursor.fetchall()
    return {"Posts": result}


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


@app.delete('/posts/{search_id}')
async def del_post(search_id: int):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"delete from posts where id={search_id}")
    conn.commit()
    return {f"product with id: {search_id} has been deleted": "Ok"}



if __name__ == "__main__":
    os.system("uvicorn main:app --reload")

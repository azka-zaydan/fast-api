import os
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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
    published: Optional[bool] = True  # set a default value
    rating: Optional[int] = 0  # make it optional


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
async def get_post_with_id(search_id: int, response: Response):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"select * from posts where id={search_id}")
    result = cursor.fetchone()
    if result is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"Post with id: {search_id}, does not exist"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {search_id}, does not exist")
    else:
        return {
            "Post": result
        }


# want title, and content both string
@app.post('/posts',status_code=status.HTTP_201_CREATED)
async def post(post: Post):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    # to_dict = post.dict() # turn into a dict
    title = post.title
    content = post.content
    cursor.execute(f"INSERT INTO posts (title,content) values ('{title}','{content}')")
    conn.commit()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1;")
    result = cursor.fetchone()
    conn.commit()
    return  {
        "post": result
    }

@app.delete('/posts/{search_id}',status_code=status.HTTP_204_NO_CONTENT)
async def del_post(search_id: int):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'select * from posts where id={search_id}')
    result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {search_id}, does not exist")
    else:
        cursor.execute(f"delete from posts where id={search_id}")
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{search_id}')
def update_post(search_id: int,post : Post):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'select * from posts where id={search_id}')
    result1 = cursor.fetchone()
    if result1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {search_id}, does not exist")
    else:
        title = post.title
        content = post.content
        cursor.execute(f"update posts set title='{title}', content='{content}' where id={search_id};")
        conn.commit()
        cursor.execute(f'select * from posts where id={search_id}')
        result = cursor.fetchone()
        return {
            "Updated Post": result
        }


if __name__ == "__main__":
    os.system("uvicorn app.main:app --reload")

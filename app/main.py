
from logging import raiseExceptions
from random import randrange
from sqlite3 import Cursor, connect
from fastapi import Body, FastAPI, HTTPException,Response,status
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    

while True:
    try:
        conn =psycopg2.connect(host='localhost',database='posts',user='postgres',password='labs',cursor_factory=RealDictCursor)
        Cursor = conn.cursor()
        print("succesful connected to database")
        break

    except Exception as error:
        print(' Could not connect to database')
        print("Error :", error)
        time.sleep(2)


my_posts =[{"title":"this is the fist title","content":"this is the first content","id":1},{"title":"this is the second title","content":"this is the second content","id":2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"]==id:
#             return p


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    Cursor.execute(""" SELECT * FROM posts""")
    posts = Cursor.fetchall()
    return {"data":posts}



@app.post("/posts" ,status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    Cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING* """, (post.title , post.content, post.published))
    new_post = Cursor.fetchone()
    conn.commit()
    return{"Data":new_post}


@app.get("/posts/{id}")
def get_post(id:int):
    Cursor.execute(""" SELECT *FROM posts WHERE id = %s""",(str(id),))
    post = Cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with an ID {id} not found')
    
    return{"post_detail": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    Cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = Cursor.fetchone()
    conn.commit()

    if deleted_post == None:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with an ID {id} not found')

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    Cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING * """,
    (post.title, post.content, post.published, str(id)))
    updated_post = Cursor.fetchone()
    conn.commit()

    if updated_post == None:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'post with an ID {id} not found')

    return{"data": updated_post}


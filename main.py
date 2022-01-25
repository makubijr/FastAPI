
from random import randrange
from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None


my_posts =[{"title":"this is the fist title","content":"this is the first content","id":1},{"title":"this is the second title","content":"this is the second content","id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    print(post)
    return{"Data":post_dict}


@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    return{"post_detail": post}
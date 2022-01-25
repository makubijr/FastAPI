
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

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_posts(post:Post):
    print(post)
    return{"Data":post}
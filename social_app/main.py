from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time 


app = FastAPI()

class Post(BaseModel):
    title: str
    content:str
    published: bool = True # default to True 
    rating: Optional[int] = None 


while True:
    try:
        conn = psycopg.connect("dbname=socialfastapidb user=postgres password=admin",row_factory=dict_row) 
        cur = conn.cursor()
        
        print("Connected to Database Successfully")
        break
    except Exception as error:
        print("Connection to DB Failed")
        print("Error",error)
        time.sleep(2)



my_posts = [{"title": "Title1", "content" : "Content1", "id": 1}, {"title": "Title2", "content" : "Content2", "id": 2}]
 
@app.get("/")
async def root():
    return {"message": "Just a bunch of Social App APIs"}

@app.get("/posts")
async def get_posts():
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:Post):
    cur.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data":new_post} 


@app.get("/posts/{id}")
def get_post(id : int):
    cur.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    post_data = cur.fetchone()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")    
    return {"data" : post_data}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute("DELETE FROM posts WHERE id=%s RETURNING *",(str(id),))
    post_data = cur.fetchone()
    conn.commit()
    if not post_data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")   
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@app.put("/posts/{id}")
def update_post(id :int, post : Post):
    cur.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *",(post.title, post.content, post.published, str(id)))
    post_date = cur.fetchone()
    conn.commit()
    if not post_date:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    return {"message": f"Post with id:{id} successfully updated", "data":post_date}


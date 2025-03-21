from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
import psycopg
from psycopg.rows import dict_row
import time 
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


# Create the tables in the DB for the models defined 
models.Base.metadata.create_all(bind=engine)




app = FastAPI()


# Connecting directly to the postgreSQL DB server through the postgreSQL driver for python - psycopg
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


 
@app.get("/")
async def root():
    return {"message": "Just a bunch of Social App APIs"}


@app.get("/posts")
async def get_posts(db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()
    
    # Using SQLAlchemy
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def create_post(post:schemas.PostCreate, db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()

    # Using SQLAlchemy
    # new_post = models.Post(title=post.title, content = post.content, published = post.published) 
    new_post = models.Post(**post.model_dump()) # Unpacking all the fields 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Identical to the RETURNING statement in SQL Query
    return {"data":new_post} 


@app.get("/posts/{id}")
def get_post(id : int, db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    # post_data = cur.fetchone()

    # Using SQLAlchemy
    post_data = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")    
    return {"data" : post_data}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("DELETE FROM posts WHERE id=%s RETURNING *",(str(id),))
    # post_data = cur.fetchone()
    # conn.commit()

    # Using SQLAlchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()
    if not post_data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")   
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@app.put("/posts/{id}")
def update_post(id :int, post : schemas.PostCreate, db: Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *",(post.title, post.content, post.published, str(id)))
    # post_date = cur.fetchone()
    # conn.commit()

    # Using SQLAlchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_date = post_query.first()
    if not post_date:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": f"Post with id:{id} successfully updated", "data":post_query.first()}


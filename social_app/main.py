from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
import psycopg
from psycopg.rows import dict_row
import time 
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session


# Create the tables in the DB for the models defined 
models.Base.metadata.create_all(bind=engine)




app = FastAPI()


# Connecting directly to the postgreSQL DB server through the postgreSQL driver for python - psycopg
# while True:
#     try:
#         conn = psycopg.connect("dbname=socialfastapidb user=postgres password=admin",row_factory=dict_row) 
#         cur = conn.cursor()
#         print("Connected to Database Successfully")
#         break
#     except Exception as error:
#         print("Connection to DB Failed")
#         print("Error",error)
#         time.sleep(2)


 
@app.get("/")
async def root():
    return {"message": "Just a bunch of Social App APIs"}


@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()
    
    # Using SQLAlchemy
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
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
    return new_post 


@app.get("/posts/{id}",response_model=schemas.PostResponse)
def get_post(id : int, db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    # post_data = cur.fetchone()

    # Using SQLAlchemy
    post_data = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")    
    return post_data


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
 

@app.put("/posts/{id}",response_model=schemas.PostResponse)
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
    return post_query.first()


@app.post("/users/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOutput)
def create_user(user : schemas.CreateUser, db: Session = Depends(get_db)):
    user_email = user.email
    user_query = db.query(models.User).filter(models.User.email == user_email)
    user_data = user_query.first()
    if user_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email:{user_email} already exist") 
    
    # Hash the user password
    hashed_pswd = utils.hash_password(user.password)
    user.password  = hashed_pswd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Identical to the RETURNING statement in SQL Query
    return new_user

@app.get("/users/{id}", response_model=schemas.UserOutput)
def get_user(id: int, db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_data = user_query.first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id:{id} not found")
    return user_data
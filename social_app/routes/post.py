from fastapi import Response, status, HTTPException, Depends , APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts"
)

@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()
    
    # Using SQLAlchemy
    posts = db.query(models.Post).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
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


@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id : int, db : Session = Depends(get_db)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    # post_data = cur.fetchone()

    # Using SQLAlchemy
    post_data = db.query(models.Post).filter(models.Post.id == id).first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")    
    return post_data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
 

@router.put("/{id}",response_model=schemas.PostResponse)
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

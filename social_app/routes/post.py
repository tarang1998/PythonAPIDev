from fastapi import Response, status, HTTPException, Depends , APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]

)

@router.get("/", response_model=List[schemas.PostOutput])
async def get_posts(db : Session = Depends(get_db),
                    curr_user : models.User  = Depends(oauth2.get_current_user),
                    limit : int = 10,
                    skip : int = 0,
                    search : Optional[str] = ""  ):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts")
    # posts = cur.fetchall()

    # posts = db.execute(
    #     'select posts.*, COUNT(votes.post_id) as votes from posts LEFT JOIN votes ON posts.id=votes.post_id  group by posts.id')

    
    # Using SQLAlchemy
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # print(posts[0]._asdict())

    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def create_post(post:schemas.PostCreate, 
                      db : Session = Depends(get_db),
                      curr_user : models.User  = Depends(oauth2.get_current_user)):
    # Using SQL Statements via psycopg
    # cur.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cur.fetchone()
    # conn.commit()

    # Using SQLAlchemy
    # new_post = models.Post(title=post.title, content = post.content, published = post.published) 
    
    new_post = models.Post(user_id = int(curr_user.id), **post.model_dump()) # Unpacking all the fields 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Identical to the RETURNING statement in SQL Query
    return new_post 


@router.get("/{id}",response_model=schemas.PostOutput)
def get_post(id : int, db : Session = Depends(get_db), curr_user : models.User  = Depends(oauth2.get_current_user)):
    # Using SQL Statements via psycopg
    # cur.execute("SELECT * FROM posts WHERE id=%s",(str(id),))
    # post_data = cur.fetchone()

    # Using SQLAlchemy
    post_data = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id, isouter=True
    ).group_by(models.Post.id).filter(models.Post.id == id,models.Post.user_id == curr_user.id).first()

    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found for user")    
    return post_data


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db),  curr_user : models.User  = Depends(oauth2.get_current_user)):
    # Using SQL Statements via psycopg
    # cur.execute("DELETE FROM posts WHERE id=%s RETURNING *",(str(id),))
    # post_data = cur.fetchone()
    # conn.commit()

    # Using SQLAlchemy
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_data = post_query.first()
    if not post_data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")   
    
    if post_data.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the requested action.")   
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id :int, post : schemas.PostCreate, db: Session = Depends(get_db),  curr_user : models.User = Depends(oauth2.get_current_user)):
    # Using SQL Statements via psycopg
    # cur.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *",(post.title, post.content, post.published, str(id)))
    # post_date = cur.fetchone()
    # conn.commit()

    # Using SQLAlchemy
    post_query = db.query(models.Post).filter(models.Post.id == curr_user.id)
    post_data = post_query.first()
    if not post_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found") 
    
    if post_data.user_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform the requested action.")   

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

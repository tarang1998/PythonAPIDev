from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/votes",
    tags= ["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote, 
         db : Session = Depends(database.get_db), 
         current_user : models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Post:{vote.post_id} not found")


    vote_query = db.query(models.Vote).filter(
              models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id)

    db_vote = vote_query.first()

    if (vote.direction == 1):
        if db_vote:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail=f"User:{current_user.id} has already voted on post:{vote.post_id}")
        
        new_vote = models.Vote(user_id = current_user.id,
                               post_id = vote.post_id)
        
        db.add(new_vote)
        db.commit()
        
        return {"message" : "Added vote successfully"}

    else:
        if not db_vote:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail=f"Vote on post:{vote.post_id} does not exist")
        
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Deleted vote successfully"}

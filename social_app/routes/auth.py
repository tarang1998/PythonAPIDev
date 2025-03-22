from fastapi import APIRouter, Depends, HTTPException, status
from .. import oauth2, schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(  
    tags=["Authentication"]
)

@router.get("/login")
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session =  Depends(get_db)):
    user_email = user_credentials.username

    # Check for the user in the DB
    user_query = db.query(models.User).filter(models.User.email == user_email)
    user_data = user_query.first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    # Verify the user password 
    if not utils.verify_pswd(user_credentials.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    # Create the JWT Token 
    access_token = oauth2.create_access_token(data={"user_id": user_data.id})

    return {"access_token": access_token, "token_type": "bearer"}

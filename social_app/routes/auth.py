from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(  
    tags=["Authentication"]
)

@router.get("/login")
def login(user_credentials : schemas.UserLogin, db : Session =  Depends(get_db)):
    user_email = user_credentials.email

    # Check for the user in the DB
    user_query = db.query(models.User).filter(models.User.email == user_email)
    user_data = user_query.first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    # Verify the user password 
    if not utils.verify_pswd(user_credentials.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    
    # Create the JWT Token 
    
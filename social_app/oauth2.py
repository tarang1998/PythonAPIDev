# from dotenv import load_dotenv
# import os
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# from pathlib import Path

# # Define the path to the .env file in the outer_folder
# env_path = Path(__file__).resolve().parent / ".env"  # Automatically points to .env in the same folder as app.py

# # Load environment variables from the specified .env file
# load_dotenv(dotenv_path=env_path)

def create_access_token(user_id : str):

    to_encode = {"user_id" : user_id} # Can add more values here 
    now = datetime.now(timezone.utc)
    # expire = now + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    expire = now + timedelta(minutes=int(settings.access_token_expire_minutes))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token : str, credentials_exception):
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])

        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))

    except InvalidTokenError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db) ):

    credential_exception =  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token : schemas.TokenData =  verify_access_token(token=token, credentials_exception=credential_exception)

    user_data = db.query(models.User).filter(models.User.id == int(token.id)).first()

    return user_data
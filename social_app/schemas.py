from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


# User models
class CreateUser(BaseModel):
    email : EmailStr
    password : str


class UserOutput(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True


# Auth models 
class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type:str

class TokenData(BaseModel):
    id : Optional[str] = None



# Post models

# Schema/Pydantic model - used to define the structure of a response and response
# Used for validation of data from the request body of the API
class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True # defaults to True 

    # rating: Optional[int] = None # optional value, defaults to None


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int 
    created_at : datetime
    user_id : int
    user : UserOutput

    class Config:
        orm_mode=True

class PostOutput(BaseModel):
    Post : PostResponse
    votes : int 
    class Config:
        orm_mode=True




# Vote models 

class Vote(BaseModel):
    post_id : int
    direction : Literal[0, 1]

    
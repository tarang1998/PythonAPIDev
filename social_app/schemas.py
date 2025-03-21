from pydantic import BaseModel


# Schema/Pydantic model - used to define the structure of a response and response
# Used for validation of data from the request body of the API
class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True # defaults to True 
    # rating: Optional[int] = None # optional value, defaults to None


class PostCreate(PostBase):
    pass
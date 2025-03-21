from fastapi import  status, HTTPException, Depends , APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users"
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOutput)
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

@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int, db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_data = user_query.first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id:{id} not found")
    return user_data
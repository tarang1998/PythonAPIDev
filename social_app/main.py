from fastapi import FastAPI
# from fastapi.params import Body
# import psycopg
# from psycopg.rows import dict_row
# import time 
from . import models
from .database import engine
from .routes import post, auth, user, vote


# SqlAlchemy Creates the tables in the DB for the models defined 
# Using Alembic instead to manage the DB schema
# models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

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


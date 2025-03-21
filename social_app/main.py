from fastapi import FastAPI
# from fastapi.params import Body
# import psycopg
# from psycopg.rows import dict_row
# import time 
from . import models
from .database import engine
from .routes import post, user


# Create the tables in the DB for the models defined 
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

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


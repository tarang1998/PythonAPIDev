from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome"}


@app.get("/posts")
async def get_posts():
    return {"data": "Post data"}
from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers import post, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

#  API starts here

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    '''
    root directory
    '''
    return 'Hello!'

# sneaky update

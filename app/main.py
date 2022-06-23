from fastapi import FastAPI
from app.apimodels import Base
from app.apidatabase import engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles as sf
from fastapi.requests import Request
from app.routers import post, user

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", sf(directory="app/static"), name="static")
app.mount('/scripts', sf(directory='app/scripts'),name='scripts')
templates = Jinja2Templates(directory='appdb-fast-api/templates')

#  API starts here

app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request':request,'title': 'Home'})

# sneaky update

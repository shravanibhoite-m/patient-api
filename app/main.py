from fastapi import  FastAPI
from fastapi_pagination import add_pagination
from dotenv import load_dotenv
from Routes import router

load_dotenv()

app=FastAPI()
app.include_router(router)
add_pagination(app)

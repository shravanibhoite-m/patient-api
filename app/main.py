from fastapi import Body, FastAPI,HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from dotenv import load_dotenv
from Routes import router

load_dotenv()

app=FastAPI()
app.include_router(router)
add_pagination(app)

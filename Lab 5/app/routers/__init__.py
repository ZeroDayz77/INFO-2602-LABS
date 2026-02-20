import os 
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.utilities import get_flashed_messages

main_router = APIRouter()
main_router.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__),"..", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__),"..", "templates"))
templates.env.globals['get_flashed_messages'] = get_flashed_messages


from .auth import auth_router
main_router.include_router(auth_router)

from .todo import todo_router
main_router.include_router(todo_router)

from .home import home_router
main_router.include_router(home_router)

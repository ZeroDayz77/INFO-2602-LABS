from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import  AuthDep
from fastapi import status

category_router = APIRouter(tags=["Category Management"])

@category_router.post("/category", response_model=CategoryResponse)
def create_category(db:SessionDep, user:AuthDep, category_data:TodoCreate):
    category = Category(text=category_data.text, user_id=user.id)
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An error occurred while creating a category",
        )

@category_router.get("/category/{cat_id}/todos", response_model=TodoResponse)
def create_category(cat_id:int, db:SessionDep, user:AuthDep):
    todos = db.exec(select(Todo).where(Category.id==cat_id)).all()
    try:
        for todo in todos:
            print(todo)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An error occurred while getting todos for cat_id = {cat_id}",
        )
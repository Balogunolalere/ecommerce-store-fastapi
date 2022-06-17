from fastapi import APIRouter, HTTPException, status, Depends
from app.models.Categories import Categories
from deta import Deta
from secrets import DETA_KEY
import maya
from app.deps import get_current_active_user
from app.models.User import (
    User,
)
from uuid import uuid4




deta = Deta(DETA_KEY)

db = deta.Base("product_categories")

user_db = deta.Base("users")


router = APIRouter()


@router.post('/categories')
async def create_categories(categories: Categories = Depends(), current_user: User = Depends(get_current_active_user)):
    try:
        user = user_db.fetch({"username": current_user['username']}).items[0]
    except IndexError:
        user = None
    if user['is_admin'] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have admin privileges"
        )
    try:
        category = db.fetch({"name": categories.name}).items[0]
    except IndexError:
        category = None
    if category is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    data_obj = dict(categories)
    data_obj["admin_user_id"] = user["id"]
    data_obj["categories_id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    data_obj['name'] = categories.name.capitalize()
    db.insert(
         data_obj,
    )
    return data_obj

@router.get('/categories/{categories_id}')
async def get_categories_id(categories_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"categories_id": categories_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this categories_id does not exist"
        )
    return user['categories']

@router.get('/categories')
async def get_categories():
    try:
        user = db.fetch().items
    except IndexError:
        user = None
    return user['categories']


@router.patch('/categories/{categories_id}')
async def update_categories(categories_id: str, categories: Categories, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"categories_id": categories_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this categories_id does not exist"
        )
    data_obj = dict(categories)
    data_obj["updated_at"] = str(maya.now())
    db.update(
        {'categories' : data_obj},
        str(user['key'])
    )
    return data_obj

@router.delete('/categories/{categories_id}')
async def delete_categories(categories_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"categories_id": categories_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this categories_id does not exist"
        )
    db.delete(
        str(user['key'])
    )
    return {"message": "deleted successfully"}

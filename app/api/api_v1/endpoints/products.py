from fastapi import APIRouter, HTTPException, status, Depends
from app.models.Products import Product
from deta import Deta
from secrets import DETA_KEY
import maya
from app.deps import get_current_active_user
from app.models.User import (
    User,
)
from uuid import uuid4




deta = Deta(DETA_KEY)

db = deta.Base("product_db")

user_db = deta.Base("users")


router = APIRouter()

@router.post('/product')
async def create_product(product: Product = Depends(), current_user: User = Depends(get_current_active_user)):
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
        product = db.fetch({"name": product.name}).items[0]
    except IndexError:
        product = None
    if product is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )
    data_obj = dict(product)
    data_obj["admin_user_id"] = user["id"]
    data_obj["product_id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    data_obj['name'] = product.name.capitalize()
    db.insert(
         data_obj,
    )
    return data_obj

@router.get('/product/{product_id}')
async def get_product_id(product_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"product_id": product_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this id does not exist"
        )
    return user

@router.get('/products')
async def get_products(current_user: User = Depends(get_current_active_user)):
    try:
        user = user_db.fetch({"username": current_user['username']}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have admin privileges"
        )
    return db.fetch({"admin_user_id": user["id"]}).items

@router.patch('/product/{product_id}')
async def update_product_id(product_id: str,product: Product = Depends(), current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"product_id": product_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this id does not exist"
        )
    data_obj = dict(product)
    data_obj["admin_user_id"] = user["id"]
    data_obj["product_id"] = str(uuid4())
    data_obj["updated_at"] = str(maya.now())
    data_obj['name'] = product.name.capitalize()
    db.insert(
         data_obj,
    )
    return data_obj

@router.delete('/product/{product_id}')
async def delete_product_id(product_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"product_id": product_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this id does not exist"
        )
    db.delete({"product_id": product_id})
    return {"message": "Product deleted successfully"}
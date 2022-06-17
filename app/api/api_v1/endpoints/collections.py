from fastapi import APIRouter, HTTPException, status, Depends
from app.models.Collections import Collection
from deta import Deta
from secrets import DETA_KEY
import maya
from app.deps import get_current_active_user
from app.models.User import (
    User,
)
from uuid import uuid4




deta = Deta(DETA_KEY)

db = deta.Base("product_collection")

user_db = deta.Base("users")


router = APIRouter()

@router.post('/collection')
async def create_collection(collection: Collection = Depends(), current_user: User = Depends(get_current_active_user)):
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
        collection = db.fetch({"name": collection.name}).items[0]
    except IndexError:
        collection = None
    if collection is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this name already exists"
        )
    data_obj = dict(collection)
    data_obj["admin_user_id"] = user["id"]
    data_obj["collection_id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    data_obj['name'] = collection.name.capitalize()
    db.insert(
         data_obj,
    )
    return data_obj

@router.get('/collection/{collection_id}')
async def get_collection_id(collection_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"collection_id": collection_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this id does not exist"
        )
    return user

@router.get('/collections')
async def get_collections(current_user: User = Depends(get_current_active_user)):
    try:
        user = user_db.fetch({"username": current_user['username']}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )
    return db.fetch({"admin_user_id": user['id']}).items

@router.patch('/collection/{collection_id}')
async def update_collection(collection_id: str, collection: Collection, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"collection_id": collection_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this id does not exist"
        )
    data_obj = dict(collection)
    data_obj["admin_user_id"] = user["id"]
    data_obj["collection_id"] = str(uuid4())
    data_obj["updated_at"] = str(maya.now())
    data_obj['name'] = collection.name.capitalize()
    db.insert(
         data_obj,
    )
    return data_obj

@router.delete('/collection/{collection_id}')
async def delete_collection(collection_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"collection_id": collection_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this id does not exist"
        )
    db.delete({"collection_id": collection_id})
    return {"message": "Collection deleted successfully"}

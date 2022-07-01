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
    except Exception:
        user = None
    if user['is_admin'] == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have admin privileges"
        )
    try:
        collection = db.fetch({"name": collection.name}).items[0]
    except Exception:
        collection = None
    if collection is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Collection with this name already exists"
        )
    data_obj = dict(collection)
    data_obj["admin_id"] = user["id"]
    data_obj["id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    data_obj['name'] = collection.name.capitalize()
    db.insert(
         data_obj,
    )
    return data_obj

@router.get('/collection/{collection_id}/')
async def get_collection_id(collection_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        collection = db.fetch({"id": collection_id}).items[0]
    except Exception:
        collection = None
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this id does not exist"
        )
    return collection

@router.get('/collections')
async def get_collections(current_user: User = Depends(get_current_active_user)):
    try:
        user = user_db.fetch({"username": current_user['username']}).items[0]
    except Exception:
        user = None
    if user['is_admin'] is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have admin privileges"
        )
    resp = [x for  x in db.fetch().items]
    return resp


@router.delete('/collection/{collection_id}')
async def delete_collection(collection_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"collection_id": collection_id}).items[0]
    except Exception:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this id does not exist"
        )
    db.delete({"collection_id": collection_id})
    return {"message": "Collection deleted successfully"}

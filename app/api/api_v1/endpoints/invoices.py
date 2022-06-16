from fastapi import APIRouter, HTTPException, status, Depends
from app.models.Invoices import Invoices
from deta import Deta
from secrets import DETA_KEY
import maya
from app.deps import get_current_active_user
from app.models.User import (
    User,
)
from uuid import uuid4




deta = Deta(DETA_KEY)

db = deta.Base("users")


router = APIRouter()

@router.post('/invoices')
async def create_invoices(invoices: Invoices, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"username": current_user['username']}).items[0]
    except IndexError:
        user = None
    data_obj = dict(invoices)
    data_obj["user_id"] = user["id"]
    data_obj["invoices_id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    db.update(
        {'invoices' : data_obj},
        str(user['key'])
    )
    return data_obj

@router.get('/invoices/{invoices_id}')
async def get_invoices(invoices_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"invoices.invoices_id": invoices_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this invoices_id does not exist"
        )
    return user['invoices']

@router.patch('/invoices/{invoices_id}')
async def update_invoices(invoices_id: str, invoices: Invoices, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"invoices.invoices_id": invoices_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this invoices_id does not exist"
        )
    data_obj = dict(invoices)
    data_obj["updated_at"] = str(maya.now())
    db.update(
        {'invoices' : data_obj},
        str(user['key'])
    )
    return data_obj

@router.delete('/invoices/{invoices_id}')
async def delete_invoices(invoices_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"invoices.invoices_id": invoices_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this invoices_id does not exist"
        )
    db.delete(
        str(user['key'])
    )
    return {"message": "deleted"}

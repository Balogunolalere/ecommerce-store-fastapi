from fastapi import APIRouter, HTTPException, status, Depends
from app.models.Orders import Orders
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

@router.post('/orders')
async def create_orders(orders: Orders = Depends(), current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"username": current_user['username']}).items[0]
    except IndexError:
        user = None
    data_obj = dict(orders)
    data_obj["user_id"] = user["id"]
    data_obj["orders_id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    db.update(
        {'orders' : data_obj},
        str(user['key'])
    )
    return data_obj

@router.get('/orders/{orders_id}')
async def get_orders(orders_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"orders.orders_id": orders_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this orders_id does not exist"
        )
    return user['orders']

@router.patch('/orders/{orders_id}')
async def update_orders(orders_id: str, orders: Orders, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"orders.orders_id": orders_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this orders_id does not exist"
        )
    return user['orders']


@router.delete('/orders/{orders_id}')
async def delete_orders(orders_id: str, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"orders.orders_id": orders_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this orders_id does not exist"
        )
    db.delete(
        {'orders' : orders_id},
        str(user['key'])
    )
    return {"message": "deleted"}
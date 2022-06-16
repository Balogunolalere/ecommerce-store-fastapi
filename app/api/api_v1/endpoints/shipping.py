from fastapi import APIRouter, HTTPException, status, Depends
from app.models.Shipping import Shipping
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


@router.post('/shipping')
async def create_shipping(shipping: Shipping, current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"username": current_user['username']}).items[0]
    except IndexError:
        user = None
    data_obj = dict(shipping)
    data_obj["user_id"] = user["id"]
    data_obj["shipping_id"] = str(uuid4())
    data_obj["created_at"] = str(maya.now())
    data_obj["updated_at"] = str(maya.now())
    db.update(
        {'shipping' : data_obj},
        str(user['key'])
    )
    #print(data)
    return data_obj
        
@router.get('/shipping/{shipping_id}') 
async def get_shipping(shipping_id: str,current_user: User = Depends(get_current_active_user)):
    try:
        user = db.fetch({"shipping.shipping_id": shipping_id}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this shipping_id does not exist"
        )
    return user['shipping']


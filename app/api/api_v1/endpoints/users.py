from fastapi import APIRouter, Depends, HTTPException, status
from app.deps import get_current_active_user
from app.models.User import (
    User,
    UserCreate,
    UserCreateResponse,
)
from uuid import uuid4
from app.utils import (
    get_password_hash
)
from secrets import (
    DETA_KEY,
)
from deta import Deta

import maya

deta = Deta(DETA_KEY)

db = deta.Base("users")






router = APIRouter()



@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post('/auth/register', response_model=UserCreateResponse)
def create_user(request:UserCreate = Depends()):
    try:
        user = db.fetch({"email": request.email}).items[0]
    except IndexError:
        user = None
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    try:
        user = db.fetch({"username": request.username}).items[0]
    except IndexError:
        user = None
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exist"
        )
    hashed_pass = get_password_hash(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_object["id"] = str(uuid4())
    data = (
        {
            'id': user_object["id"],
            'username': user_object["username"],
            'email': user_object["email"],
            'password': user_object["password"],
            'first_name': str(user_object["first_name"]).capitalize(),
            'last_name': str(user_object["last_name"]).capitalize(),
            'phone': user_object["phone"],
            'address': str(user_object["address"]).capitalize(),
            'city': str(user_object["city"]).capitalize(),
            'state': str(user_object["state"]).capitalize(),
            'country': str(user_object["country_code"]).upper(),
            'created_at' : str(maya.now()),
            'zip': user_object["zip"],
            'disabled' : False,
            'is_admin' : False,
        }
    )
    user= db.insert(data)

    return user
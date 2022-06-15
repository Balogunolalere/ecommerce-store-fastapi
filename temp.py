from fastapi import APIRouter, Depends, HTTPException, status
from app.deps import get_current_active_user
from app.models.User import (
    User,
    UserCreate,
    UserCreateResponse,
)
from app.utils import (
    get_password_hash
)
from secrets import (
    DETA_KEY,
)
from deta import Deta

deta = Deta(DETA_KEY)

db = deta.Base("users")





router = APIRouter()



@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post('/auth/register', response_model=UserCreateResponse)
def create_user(request:UserCreate):
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
    user= db.insert(user_object)

    return {"res":"created", 'user_details': user_object}  
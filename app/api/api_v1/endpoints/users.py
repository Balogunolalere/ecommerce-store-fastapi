from fastapi import APIRouter, HTTPException, Depends, Request,status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.User import User
from fastapi.responses import RedirectResponse
from uuid import uuid4
from deta import Deta  # Import Deta
from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from secrets import DETA_KEY


# Initialize with a Project Key
deta = Deta(DETA_KEY)

# This how to connect to or create a database.
db = deta.Base("users")

router = APIRouter()

@router.post('/auth/register')
async def create_user(request:User):
    # querying database to check if user already exist
    #user = db.get(data.email, None)
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
    hashed_pass = get_hashed_password(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_object["id"] = str(uuid4())
    user= db.insert(user_object)

    return {"res":"created", 'user_details': user_object}        # return the user id



@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = db.fetch({"username": form_data.username}).items[0]
    except IndexError:
        user = None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
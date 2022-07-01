from fastapi import FastAPI, Depends, HTTPException, status
from app.api.api_v1.api import router as api_router
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.models.User import (
    Token,
)
from app.utils import (
    create_access_token,
    verify_password,

)
from secrets import (
    DETA_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from deta import Deta

deta = Deta(DETA_KEY)

db = deta.Base("users")




app = FastAPI(
    description='simple ecommerce api',
    version="0.0.1",
    contact={
        "name": "bandersnatchx64",
        "url": "https://twitter.com/bandersnatchx64",
        "email": "lordareello@gmail.com",
    },
)


@app.post("/token", response_model=Token, tags=["User"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = db.fetch({"username": form_data.username}).items[0]
    except IndexError:
        user = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = user['password']
    if not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root():
    return {"message": "Hello World"}



app.include_router(api_router, prefix='/api/v1')
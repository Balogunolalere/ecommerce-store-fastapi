from fastapi import APIRouter, HTTPException, Depends, Request,status
from hashing import Hash
from app.models.User import User
from jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from oauth import get_current_user
from deta import Deta  # Import Deta



# Initialize with a Project Key
deta = Deta("a0w8cydc_LMiMFDHopaxhCNkBqiJoXJRkZcbh7n9M")

# This how to connect to or create a database.
db = deta.Base("users")

router = APIRouter()

@router.post('/auth/register')
def create_user(request:User):
   hashed_pass = Hash.bcrypt(request.password)
   user_object = dict(request)
   user_object["password"] = hashed_pass
   user= db.insert(user_object)

   return {"res":"created", 'user_details': user_object}        # return the user id


@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    user = db.fetch({"username": request.username}).items[0]
    #user = db["users"].find_one({"username":request.username})
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}
    


@router.get('/user')
def get_user(current_user: User = Depends(get_current_user)):
    return {"user": current_user}
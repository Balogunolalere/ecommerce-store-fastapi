#from datetime import datetime
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Union
import re
import maya


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=3, max_length=50)
    email : EmailStr
    first_name : str = Field(..., min_length=3, max_length=50)
    last_name : str = Field(..., min_length=3, max_length=50)
    phone : str = Field(..., min_length=3, max_length=50)
    address : str = Field(..., min_length=3, max_length=200)
    city : str = Field(..., min_length=3, max_length=50)
    state : str = Field(..., min_length=3, max_length=50)
    zip : str = Field(..., min_length=3, max_length=50)
    country_code : str = Field(..., min_length=2, max_length=5)
    disabled : bool = False

    @validator('phone')
    def validate_phone(cls, v):
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if v and not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v

class UserCreateResponse(BaseModel):
    username: Union[str, None] = None
    id : Union[str, None] = None
    email : Union[EmailStr, None] = None
    first_name : Union[str, None] = None
    last_name : Union[str, None] = None
    phone : Union[str, None] = None
    address : Union[str, None] = None
    city : Union[str, None] = None
    state : Union[str, None] = None
    zip : Union[str, None] = None
    country : Union[str, None] = None
    disabled : Union[bool, None] = None
    created_at : Union[str, None] = None



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    id : Union[str, None] = None
    username: str
    email: Union[EmailStr, None] = None
    disabled: Union[bool, None] = None




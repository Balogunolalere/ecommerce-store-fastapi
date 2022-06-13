from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    id : int
    email : str
    first_name : str
    last_name : str
    phone : str
    address : str
    city : str
    state : str
    zip : str
    country : str
    #created_at : Optional[datetime] = datetime.now()
    disabled : bool = False

class Login(BaseModel):
    username: str
    password: str
    

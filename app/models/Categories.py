from typing import List
from typing import Optional
from pydantic import BaseModel


class Categories(BaseModel):
    id : Optional[int] = None
    admin_id : Optional[str] = None
    name : str
    description : Optional[str] = None
    created_at : Optional[str] = None
    updated_at : Optional[str] = None

class CategoriesUpdate(BaseModel):
    name : str
    description : str
    updated_at : Optional[str] = None
    


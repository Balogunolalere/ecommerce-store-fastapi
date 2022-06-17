from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel

class Collection(BaseModel):
    id : int
    name: str
    created_by: str

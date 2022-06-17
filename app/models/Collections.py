from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel

class Collection(BaseModel):
    name: str

from typing import Optional
from pydantic import BaseModel

class Collection(BaseModel):
    id : Optional[str] = None
    admin_id : Optional[str] = None
    name: str
    date_created: Optional[str] = None
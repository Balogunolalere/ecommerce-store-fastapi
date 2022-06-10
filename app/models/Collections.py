from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel

class Collection(BaseModel):
    id : int
    name: str
    created_by: str
    date_created : Optional[datetime] = datetime.now()
    created_by : str
    date_updated : Optional[datetime] = datetime.now()
    updated_by : str

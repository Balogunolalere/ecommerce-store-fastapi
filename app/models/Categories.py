from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel


class Categories(BaseModel):
    id : int
    name : str
    created_at : Optional[datetime] = datetime.now()
    created_by : str
    updated_at : Optional[datetime] = datetime.now()
    updated_by : str
    
    


from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel


class Shipping(BaseModel):
    id : int
    user_id : int
    address : str
    city : str
    state : str
    zip_code : str
    country : str
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()
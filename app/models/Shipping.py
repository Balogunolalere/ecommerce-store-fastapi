from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel


class Shipping(BaseModel):
    address : str
    city : str
    state : str
    zip_code : str
    country : str
    
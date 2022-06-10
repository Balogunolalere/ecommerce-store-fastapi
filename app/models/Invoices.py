from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel

from app.models.Shipping import Shipping



class Invoices(BaseModel):
    id : int
    user_id : int
    payment_status : str
    discount : float
    shipping_fee : float
    tax_fee : float
    shipping_id : int
    payment_method : str
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()
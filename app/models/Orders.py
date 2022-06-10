from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel


class Orders(BaseModel):
    id: int
    user_id: int
    shipping_id: int
    cart_id : int
    product_id : int
    quantity : int
    payment_method : str
    total: float
    status: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
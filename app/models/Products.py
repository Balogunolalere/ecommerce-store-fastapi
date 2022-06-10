from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    id : int
    name : str
    description : str
    price : float
    available_quantity : int
    tags : List[str]
    created_at : Optional[datetime] = datetime.now()
    updated_at : Optional[datetime] = datetime.now()
    created_by : str
    updated_by : str
    product_manufacturer : str
    product_brand_name : str
    product_collection : str
    product_category : str





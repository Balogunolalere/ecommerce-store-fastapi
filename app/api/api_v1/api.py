from fastapi import APIRouter

from .endpoints import (
    shipping,
    products,
    orders,
    invoices,
    collections,
    category,
    users,
)


router = APIRouter()

router.include_router(shipping.router, prefix='/shipping', tags=['Shipping'])
# router.include_router(products.router, prefix='/products', tags=['Products'])
router.include_router(orders.router, prefix='/orders', tags=['Orders'])
router.include_router(invoices.router, prefix='/invoices', tags=['Invoices'])
# router.include_router(collections.router, prefix='/collections', tags=['Collections'])
router.include_router(category.router, prefix='/categories', tags=['Categories'])
router.include_router(users.router, prefix='/users', tags=['User'])


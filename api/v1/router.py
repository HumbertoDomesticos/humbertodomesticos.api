from fastapi import APIRouter
from .endpoints.produtos import router as prod_router
from .endpoints.categorias import router as cat_router

router = APIRouter()

router.include_router(prod_router)
router.include_router(cat_router)
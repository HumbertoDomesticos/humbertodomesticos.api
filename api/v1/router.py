from fastapi import APIRouter
from .endpoints.produtos import router as prod_router
from .endpoints.categorias import router as cat_router
from .endpoints.usuarios import router as usuario_router

router = APIRouter()

router.include_router(prod_router)
router.include_router(cat_router)
router.include_router(usuario_router)
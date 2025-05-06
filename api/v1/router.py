from fastapi import APIRouter
from .endpoints.produtos import router as prod_router

router = APIRouter()

router.include_router(prod_router)
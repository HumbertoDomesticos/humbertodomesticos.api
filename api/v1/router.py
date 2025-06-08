from fastapi import APIRouter
from .endpoints.categorias import router as categoria_router
from .endpoints.produtos import router as produto_router
from .endpoints.usuarios import router as usuario_router
from .endpoints.pedidos import router as pedido_router

router = APIRouter()

router.include_router(categoria_router)
router.include_router(produto_router)
router.include_router(usuario_router)
router.include_router(pedido_router)
from fastapi import APIRouter
from .endpoints.produtos import router as prod_router
from .endpoints.categorias import router as cat_router
from .endpoints.usuarios import router as usuario_router
from .endpoints.pedidos import router as pedido_router
from .endpoints.enderecos import router as endereco_router
from .endpoints.telefones import router as telefone_router

router = APIRouter()

router.include_router(prod_router)
router.include_router(cat_router)
router.include_router(usuario_router)
router.include_router(pedido_router)
router.include_router(endereco_router)
router.include_router(telefone_router)
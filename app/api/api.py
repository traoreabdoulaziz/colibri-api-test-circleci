from fastapi import APIRouter

from .endpoints import services, auth
router = APIRouter()


router.include_router(services.router)
router.include_router(auth.auth_router)


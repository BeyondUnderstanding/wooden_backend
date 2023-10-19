from fastapi import APIRouter
from .auth.router import admin_auth_router
from .games.router import games_router
from .objectstorage.router import s3router
from .images.router import imagerouter

admin_router = APIRouter(prefix='/admin')

admin_router.include_router(admin_auth_router)
admin_router.include_router(games_router)
admin_router.include_router(s3router)
admin_router.include_router(imagerouter)


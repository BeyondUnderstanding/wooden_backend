from fastapi import APIRouter
from .admin.router import admin_router


main_router = APIRouter(prefix='/v1')
main_router.include_router(admin_router)

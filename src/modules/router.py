from fastapi import APIRouter
from .admin.router import admin_router
from .client.router import client
from .integrations.cryptocom.router import cryptocom

main_router = APIRouter(prefix='/v1')
main_router.include_router(admin_router)
main_router.include_router(client)
main_router.include_router(cryptocom)
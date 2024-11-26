from fastapi import APIRouter

from api.v1.file import file_routers

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(file_routers)

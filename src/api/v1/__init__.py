from api.v1.file import file_routers
from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(file_routers)

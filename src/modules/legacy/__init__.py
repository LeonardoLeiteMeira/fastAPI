from fastapi import APIRouter
from .controller import router

legacy_data_router = APIRouter()

legacy_data_router.include_router(router)

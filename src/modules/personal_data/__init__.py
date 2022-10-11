from fastapi import APIRouter
from .controller import router

personal_data_router = APIRouter()

personal_data_router.include_router(router)
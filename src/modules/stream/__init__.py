from fastapi import APIRouter
from .controller import router

stream_router = APIRouter()
stream_router.include_router(router)
from fastapi import APIRouter
from .controller import router

super_heros_router = APIRouter()
super_heros_router.include_router(router)
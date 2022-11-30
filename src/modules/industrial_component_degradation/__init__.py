from fastapi import APIRouter
from .controller import router

industry_component_router = APIRouter()

industry_component_router.include_router(router)
from fastapi import APIRouter

from .fast_api_tests_controller import health_router

fast_api_tests_routers = APIRouter()

fast_api_tests_routers.include_router(health_router)

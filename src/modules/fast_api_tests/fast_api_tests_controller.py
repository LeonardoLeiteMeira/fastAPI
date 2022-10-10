from fastapi import APIRouter, status

from base_models.base_models import ModelName


from .app_service import AppService

health_router = APIRouter(tags=["fast_api_test"])

@health_router.get("/")
async def root():
    return {"message": "Access /docs to see the documentation"}

@health_router.get("/health-check", status_code=status.HTTP_200_OK)
def get_health_check():
    service = AppService()
    return service.health_check()

@health_router.get("/items/{id}")
async def items(id: int):
    return {
        "phone": {
            "id": id,
            "name": "iPhone 12",
            "memory": 128,
            "user": "Leonardo Leite",
        },
    }


@health_router.get("/models_description/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.artur or model_name is ModelName.laura:
        return {"response": "Brothers"}

    if model_name is ModelName.alice or model_name is ModelName.cicero:
        return {"response": "Parents"}

    if model_name is ModelName.leo:
        return {"response": "It's me"}


@health_router.get("/base_models/")
async def get_models(mySelf: bool, brothers: bool | None = True):
    response: dict = {}
    response["Parents"] = {"Mother": ModelName.alice.value, "Father": ModelName.cicero.value}

    if mySelf is True:
        response["Me"] = ModelName.leo

    if brothers is True:
        response["Brothers"] = {"Sister": ModelName.laura.value, "Brother": ModelName.artur.value}

    return response

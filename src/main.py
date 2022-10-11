from base_models.base_models import ModelName
from base_models.models import Person
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from modules.fast_api_tests import fast_api_tests_routers
from modules.personal_data import personal_data_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(fast_api_tests_routers)
app.include_router(personal_data_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

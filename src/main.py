from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.modules.fast_api_tests import health_router
from src.modules.personal_data import personal_data_router
from src.modules.industrial_component_degradation import industry_component_router
from src.modules.legacy import legacy_data_router
from src.modules.stream import stream_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(health_router,prefix="/test")
app.include_router(industry_component_router,prefix="/industrial")
app.include_router(personal_data_router,prefix="/personal")
app.include_router(legacy_data_router,prefix="/legacy")
app.include_router(stream_router,prefix="/stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

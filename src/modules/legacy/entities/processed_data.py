from bson import ObjectId
from pydantic import BaseModel, Field
from base_models.base_models import PyObjectId
from modules.legacy.entities.stop_reason_data import StopReasonData

class ProcessedData(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    file:str = Field(...)
    result:list[StopReasonData] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
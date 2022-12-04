from bson import ObjectId
from pydantic import BaseModel, Field

class StopReasonData(BaseModel):
    reason:str = Field(...)
    duration_total:str = Field(...)
    relative_duration:float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
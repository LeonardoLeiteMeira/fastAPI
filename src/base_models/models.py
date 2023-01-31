from pydantic import BaseModel, Field
from bson import ObjectId
from src.base_models.base_models import PyObjectId


class Person(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    lastname: str = Field(...)
    country: str | None = Field(...)
    city: str | None = Field(None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
